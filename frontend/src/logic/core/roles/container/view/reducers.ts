import { produce } from 'immer';

import type { ReducersDef } from '@/logic';

import type { RoleViewContainerLogic } from './type';

export const Reducers: ReducersDef<RoleViewContainerLogic> = {
  entries: [
    new Map(),
    {
      addEntries: (immutableState, { entries }) =>
        produce(immutableState, (state) => {
          for (const entry of entries) {
            state.set(entry.id, entry);
          }
        }),
      removeEntries: (immutableState, { entryIds }) =>
        produce(immutableState, (state) => {
          for (const id of entryIds) {
            state.delete(id);
          }
        }),
    },
  ],
  usageCounters: [
    new Map(),
    {
      addEntries: (immutableState, { entries }) =>
        produce(immutableState, (state) => {
          for (const entry of entries) {
            state.set(entry.id, { counter: 0, lastUseTime: new Date() });
          }
        }),
      removeEntries: (immutableState, { entryIds }) =>
        produce(immutableState, (state) => {
          for (const entryId of entryIds) {
            state.delete(entryId);
          }
        }),
      useEntries: (immutableState, { entryIds }) =>
        produce(immutableState, (state) => {
          for (const entryId of entryIds) {
            const usageCounter = state.get(entryId);
            if (usageCounter != null) {
              usageCounter.counter++;
              usageCounter.lastUseTime = new Date();
            } else {
              throw Error(
                'Using an entry that is not present in the container.',
              );
            }
          }
        }),
      releaseEntries: (immutableState, { entryIds }) =>
        produce(immutableState, (state) => {
          for (const entryId of entryIds) {
            const usageCounter = state.get(entryId);
            if (usageCounter != null) {
              usageCounter.counter--;
              usageCounter.lastUseTime = new Date();
            } else {
              throw Error(
                'Releasing an entry that is not present in the container.',
              );
            }
          }
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
};
