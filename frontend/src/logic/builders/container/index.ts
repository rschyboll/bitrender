import { produce } from 'immer';
import { BuiltLogic, LogicWrapper } from 'kea';
import {
  LogicBuilder,
  actions,
  afterMount,
  beforeUnmount,
  getContext,
  listeners,
  reducers,
} from 'kea';

import type {
  ContainerBuilderInput,
  MakeContainerBuilderLogicType,
} from './type';

export * from './type';
export * from './interface';

/**
 * Container logic builder, it is used to create a logic that serves as a container.
 *
 * A container logic has multiple purposes:
 * - Stores some data (entries) that are used in other parts of the application.
 * - Automatically cleans this data when it is no longer used (after a delay defined in the builder input).
 * - Remains mounted for some time after the last logic stops using it, so that the data stored in it doesn't
 *    disappear immediately.
 *
 * This kind of logic allows for easy design of the store with the single source of truth principle.
 * With this structure, any logic can first check if some data is already loaded. If it isn't, the logic can
 * then load the data from the backend. This reduces the number of requests to the backend, and in the future,
 * it may even be possible to use a websocket that would automatically update the data in the container, which
 * would then update the data everywhere in the application.
 *
 * @param input - The config for the container, or a function, that accepts the logic and returns the config.
 *                The config defines how the container should behave. See the {@link ContainerBuilderInput} type
 *                for more details. *
 * @returns The logic builder, which creates all necessary properties on the logic.
 */
export function container<Logic extends MakeContainerBuilderLogicType>(
  input: ContainerBuilderInput | ((logic: Logic) => ContainerBuilderInput),
): LogicBuilder<Logic> {
  /**
   * This is the logic builder, used by kea to create a logic in the kea function.
   * It creates all necessary properties of the logic by calling other logic builders or by directly editing it.
   */
  return (logic) => {
    const config = typeof input === 'function' ? input(logic) : input;

    /**
     * If this intended behavior for your use case, then you can safely remove this warning.
     */
    if (config.dataCleanTimeout > config.unmountDelay) {
      console.warn(
        `In the ${logic.pathString} container, \
the dataCleanTimeout (${config.dataCleanTimeout}) \
is bigger than the unmountDelay (${config.unmountDelay}).\

This could lead to some undesired behavior, as the container may unmount,\
with some entries still present in it.`,
      );
    }
    /**
     * This simply creates all the actions used by the container. There's nothing special going on here.
     */
    actions<MakeContainerBuilderLogicType>({
      startGarbageCollection: true,
      stopGarbageCollection: true,
      startMountWatcher: true,
      stopMountWatcher: true,
      addEntries: (entries) => ({ entries }),
      removeEntries: (entryIds) => ({ entryIds }),
      useEntries: (entryIds) => ({ entryIds }),
      releaseEntries: (entryIds) => ({ entryIds }),
      updateEntries: (entries) => ({ entries }),
      forceCleanup: true,
    })(logic);

    /**
     * This creates all the reducers used in the container and defines how the values should change in response
     * to dispatched actions.
     */
    reducers<MakeContainerBuilderLogicType>({
      entries: [
        new Map(),
        {
          /**
           * Adds entries to the reducer. If the entries are already in the container,
           * then it overrides them.
           */
          addEntries: (immutableState, { entries }) =>
            produce(immutableState, (state) => {
              forEntry(entries, (id, entry) => {
                state.set(id, entry);
              });
            }),
          /**
           * Removes entries from the reducer. It should not be called directly; it is only called by the garbage
           * collection process or by calling the forceCleanup action.
           */
          removeEntries: (immutableState, { entryIds }) =>
            produce(immutableState, (state) => {
              forIds(entryIds, (id) => {
                state.delete(id);
              });
            }),
        },
      ],
      usageCounters: [
        new Map(),
        {
          /**
           * Creates usage counters for the entries added to the container. By default, a new entry has a counter of 0
           * and the lastUseTime set to the current date, so it won't be removed immediately.
           */
          addEntries: (immutableState, { entries }) =>
            produce(immutableState, (state) => {
              const currentDate = new Date();
              forEntry(entries, (id) => {
                state.set(id, { counter: 0, lastUseTime: currentDate });
              });
            }),
          /**
           * Removes usage counters for entries that have been removed from the container.
           */
          removeEntries: (immutableState, { entryIds }) =>
            produce(immutableState, (state) => {
              for (const entryId of entryIds) {
                state.delete(entryId);
              }
            }),
          /**
           * Marks the entries as used by increasing their usageCounter by one and updating their lastUseTime.
           *
           * @throws {@link Error}
           * If a id in entryIds is not present in the container, this error is thrown. This represents a dev error,
           * as it should not be possible to use an entry that is not in the container.
           */
          useEntries: (immutableState, { entryIds }) =>
            produce(immutableState, (state) => {
              forIds(entryIds, (id) => {
                const usageCounter = state.get(id);
                if (usageCounter != null) {
                  usageCounter.counter++;
                  usageCounter.lastUseTime = new Date();
                } else {
                  throw Error(
                    'Using an entry, that is not present in the container.',
                  );
                }
              });
            }),
          /**
           * Releases the entries by decreasing their usageCounter by one and updating their lastUseTime.
           *
           * The last use time is updated here because updating it only in the useEntries counter could result in the
           * entry being removed immediately after releasing it.
           *
           * @throws {@link Error}
           * If a id in entryIds is not present in the container, this error is thrown. This represents a dev error,
           * as it should not be possible to release an entry that is not in the container.
           */
          releaseEntries: (immutableState, { entryIds }) =>
            produce(immutableState, (state) => {
              forIds(entryIds, (id) => {
                const usageCounter = state.get(id);
                if (usageCounter != null) {
                  if (usageCounter.counter > 0) {
                    usageCounter.counter -= 1;
                    usageCounter.lastUseTime = new Date();
                  }
                } else {
                  throw Error(
                    'Releasing an entry, that is not present in the container.',
                  );
                }
              });
            }),
        },
      ],
      garbageCollectionRunning: [
        false,
        {
          startGarbageCollection: () => true,
          stopGarbageCollection: () => false,
        },
      ],
      mountWatcherRunning: [
        false,
        {
          startMountWatcher: () => true,
          stopMountWatcher: () => false,
        },
      ],
    })(logic);

    listeners<LogicWrapper<MakeContainerBuilderLogicType>>(
      ({ actions, values, pathString, mount, unmount }) => ({
        /**
         * This listener performs the garbage collection process for the container.
         * It loops until the `garbageCollectionRunning` flag is set to `true`, and at each iteration,
         * it checks the usage counters for each entry in the container.
         *
         * If an entry's usage counter is less than or equal to 0 and the time since
         * its last use is greater than or equal to the `dataCleanTimeout` specified in the config, the entry is
         * removed from the container. The function also waits for a short time between iterations to avoid using
         * excessive CPU time.
         */
        startGarbageCollection: async (_, breakpoint) => {
          while (values.garbageCollectionRunning) {
            const currentTime = new Date();
            const deviceIdsToRemove: string[] = [];
            for (const deviceKey in values.usageCounters) {
              const usageCounter = values.usageCounters.get(deviceKey);
              if (
                usageCounter != null &&
                usageCounter.counter <= 0 &&
                currentTime.getTime() - usageCounter.lastUseTime.getTime() >=
                  config.dataCleanTimeout
              ) {
                deviceIdsToRemove.push(deviceKey);
              }
            }
            if (deviceIdsToRemove.length > 0) {
              actions.removeEntries(deviceIdsToRemove);
            }
            await breakpoint(config.dataCleanTimeout / 5);
          }
        },
        /**
         * This code runs a loop that monitors the mount status of the logic and delays its unmounting for a specified
         * delay. The `mountWatcherRunning` flag determines whether the loop should continue running.
         *
         * When the logic gets mounted, it mounts itself one additional time and then monitors its mount counter. If the
         * mount counter drops to 1, which implies that the only mount is the one that the logic performed itself, it
         * remembers the date when it happened. When the specified amount of time (in the config) passes from that date,
         * the logic unmounts itself.
         *
         * The code also waits for a short time between iterations to avoid using excessive CPU time.
         */
        startMountWatcher: async (_, breakpoint) => {
          let unmountDate: null | Date = null;
          mount();
          while (values.mountWatcherRunning) {
            const { mount } = getContext();
            const counters = mount.counter;
            const logicCounter = counters[pathString];

            if (logicCounter >= 1 && unmountDate == null) {
              unmountDate = new Date();
            }
            if (logicCounter != 1 && unmountDate != null) {
              unmountDate = null;
            }
            if (
              logicCounter == 1 &&
              unmountDate != null &&
              new Date().getTime() - unmountDate.getTime() > config.unmountDelay
            ) {
              unmount();
              break;
            }
            await breakpoint(config.dataCleanTimeout / 5);
          }
        },
        forceCleanup: async () => {
          const deviceIdsToRemove: string[] = [];

          for (const deviceKey in values.usageCounters) {
            const usageCounter = values.usageCounters.get(deviceKey);
            if (usageCounter != null && usageCounter.counter <= 0) {
              deviceIdsToRemove.push(deviceKey);
            }
          }

          actions.removeEntries(deviceIdsToRemove);
        },
      }),
    )(
      logic as unknown as BuiltLogic<
        LogicWrapper<MakeContainerBuilderLogicType>
      >,
    );

    afterMount<MakeContainerBuilderLogicType>(({ actions }) => {
      actions.startGarbageCollection();
      actions.startMountWatcher();
    })(logic);

    beforeUnmount<MakeContainerBuilderLogicType>(({ actions }) => {
      actions.stopGarbageCollection();
      actions.stopMountWatcher();
    })(logic);

    return logic;
  };
}

/**
 * Calls a callback function for each entry in a map, record, or array of objects.
 *
 * The `callback` function is called for each entry and is passed two arguments:
 * - the entry's ID
 * - the entry's value.
 *
 * The ID is either the key of the entry in the map,
 * the property name of the entry in the record, or the `id` property of the entry
 * in the array.
 *
 * The value is the corresponding entry in the map, record, or array.
 *
 * The function is used in the {@link container} builder, to iterate over entries,
 * that are beeing added to the container.
 *
 * @param entries - The map, record, or array to iterate over. The objects in the
 *   array must have an `id` property.
 * @param callback - The function to call for each entry.
 *   It will be passed the entry's `id` and the entry itself.
 */
function forEntry(
  entries: Map<string, unknown> | Record<string, unknown> | { id: string }[],
  callback: (id: string, entry: unknown) => void,
) {
  if (Array.isArray(entries)) {
    for (const entry of entries) {
      callback(entry.id, entry);
    }
  } else if (entries instanceof Map) {
    entries.forEach((entry, id) => {
      callback(id, entry);
    });
  } else {
    for (const id in entries) {
      callback(id, entries[id]);
    }
  }
}

/**
 * Calls a callback function for each id in an array or set of ids as strings.
 *
 * The function is used in the {@link container} builder, to iterate over entry ids,
 * that are already in the container, but are beeing manipulated somehow.
 *
 * @param entryIds - The array or set of ids to iterate over.
 * @param callback - The function to call for each id. It will be passed the id as a string.
 */
function forIds(
  entryIds: string[] | Set<string>,
  callback: (id: string) => void,
) {
  if (entryIds instanceof Set) {
    entryIds.forEach((id) => {
      callback(id);
    });
  } else {
    for (const id of entryIds) {
      callback(id);
    }
  }
}
