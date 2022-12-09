import type { container } from '@/logic/builders';
import type { MakeOwnLogicType } from '@/logic/types/';

interface Actions<EntryType> {
  /**
   * Starts the garbage collection process. Should not be used directly.
   * It is launched automatically in the afterMount event.
   */
  startGarbageCollection: true;
  /**
   * Stops the garbage collection process. Should not be used directly.
   * It is launched automatically in the beforeUnmount event.
   */
  stopGarbageCollection: true;
  /**
   * Adds new entries to the container.
   *
   * @param entries
   * A map, record, or array of entries to add to the store.
   *
   * If an entry has an `id` property and the entries are passed as an array,
   * the `id` property will be used as the key for the entry in the container.
   *
   * If the entries are passed as a `Record` or `Map` object,
   * the keys of the object will be used as the keys for the entries in the container.
   */
  addEntries: (
    entries: EntryType extends { id: string }
      ? Map<string, EntryType> | Record<string, EntryType> | EntryType[]
      : Map<string, EntryType> | Record<string, EntryType>,
  ) => {
    entries: EntryType extends { id: string }
      ? Map<string, EntryType> | Record<string, EntryType> | EntryType[]
      : Map<string, EntryType> | Record<string, EntryType>;
  };
  /**
   * Removes the specified entries from the container.
   *
   * @param entryIds
   * An array or set of entry ids to remove from the container.
   */
  removeEntries: (entryIds: string[] | Set<string>) => {
    entryIds: string[] | Set<string>;
  };
  /**
   * Marks the specified entries as "used" in the container.
   * This will prevent the entries from being garbage collected until they are released.
   *
   * @param entryIds
   * An array or set of entry ids to mark as "used" in the container.
   */
  useEntries: (entryIds: string[] | Set<string>) => {
    entryIds: string[] | Set<string>;
  };
  /**
   * Marks the specified entries as "unused" in the container.
   * This will allow the entries to be garbage collected if they are not needed by any other part of the application.
   *
   * @param entryIds
   * An array or set of entry ids to mark as "unused" in the container.
   */
  releaseEntries: (entryIds: string[] | Set<string>) => {
    entryIds: string[] | Set<string>;
  };
  /**
   * Updates the specified entries in the container.
   *
   * This action does not change the usageCounter of the entries, it only updates their values.
   *
   * @param entries
   * A map, record, or array of entries to update in the container.
   *
   * If an entry has an `id` property and the entries are passed as an array,
   * the `id` property will be used as the key for the entry in the container.
   *
   * If the entries are passed as a `Record` or `Map` object,
   * the keys of the object will be used as the keys for the entries in the container.
   */
  updateEntries: (
    entries: EntryType extends { id: string }
      ? Map<string, EntryType> | Record<string, EntryType> | EntryType[]
      : Map<string, EntryType> | Record<string, EntryType>,
  ) => {
    entries: EntryType extends { id: string }
      ? Map<string, EntryType> | Record<string, EntryType> | EntryType[]
      : Map<string, EntryType> | Record<string, EntryType>;
  };
  /**
   * Starts the mount watcher. This should not be used directly.
   * It is launched automatically in the afterMount event.
   */
  startMountWatcher: true;
  /**
   * Stops the mount watcher. This should not be used directly.
   * It is launched automatically in the beforeUnmount event.
   */
  stopMountWatcher: true;

  /**
   * Forces the garbage collection process to run immediately,
   * without waiting for the next garbage collection loop.
   *
   * It ignores the `lastUseTimes`, and removes all entries, that are currently unused.
   *
   * This can be used, for example, when a user logs out and should
   * no longer have access to any of the entries in the container.
   */
  forceCleanup: true;
}

interface Reducers<EntryType> {
  /**
   * A `Map` object that holds the entries in the container,
   * with the keys being the `id` property of the entries
   * and the values being the entries themselves.
   */
  entries: Map<string, EntryType>;
  /**
   * A `Map` object that holds a usage counter and last use time for each entry in the container.
   *
   * The keys of the `Map` are the `id` property of the entries, and the values are objects containing
   * the counter and last use time for each entry.
   */
  usageCounters: Map<string, { counter: number; lastUseTime: Date }>;
  /**
   * A boolean value that indicates whether the garbage collection process is currently running.
   */
  garbageCollectionRunning: boolean;
  /**
   * A boolean value that indicates whether the mount watcher is currently running.
   * */
  mountWatcherRunning: boolean;
}

/**
 * The `ContainerBuilderInput` interface defines the input, to the {@link container} builder.
 */
export interface ContainerBuilderInput {
  /**
   * The amount of time, in milliseconds, after which unused entries will be removed from the container.
   */
  dataCleanTimeout: number;
  /**
   * The amount of time, in milliseconds, to wait after the container is no longer in use before
   * stopping the garbage collection process and removing the container from memory.
   */
  unmountDelay: number;
}

/**
 * The `MakeContainerBuilderLogicType` type is used to create a container logic type.
 * It takes one generic argument `EntryType`, it defines the type of entry, stored in the container.
 *
 * It is used together with the {@link container} builder, to create a container logic.
 *
 * @typeParam EntryType - Type of entries, stored in the container.
 */
export type MakeContainerBuilderLogicType<EntryType = any> = MakeOwnLogicType<{
  actions: Actions<EntryType>;
  reducers: Reducers<EntryType>;
}>;
