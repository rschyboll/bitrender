import { MakeOwnLogicType } from '@/logic/types';

import { MakeContainerBuilderLogicType } from './type';

/**
 * This interface defines a type that specifies a subset of the actions and reducers
 * available in the `MakeContainerBuilderLogicType` interface, based on the provided
 * type parameters.
 *
 * It is used to create a interface, that exposes only some of the actions and reducers in the container logic.
 * It allows to use it with a DI system, like inversify.js {@link https://inversify.io/} used in this project.
 *
 * @typeParam EntryType - Type of entries, stored in the container.
 * @typeParam Actions - A subset of the actions available in the `MakeContainerBuilderLogicType` interface,
 *  that should be used in the interface.
 * @typeParam Reducers - A subset of the reducers available in the `MakeContainerBuilderLogicType` interface,
 *  that should be used in the interface.
 */
export type MakeContainerBuilderLogicInterface<
  EntryType,
  Actions extends keyof MakeContainerBuilderLogicType<EntryType>['actions'] =
    | 'addEntries'
    | 'useEntries'
    | 'releaseEntries'
    | 'updateEntries'
    | 'forceCleanup',
  Reducers extends keyof MakeContainerBuilderLogicType<EntryType>['reducers'] = 'entries',
> = MakeOwnLogicType<{
  actions: Pick<MakeContainerBuilderLogicType<EntryType>['actions'], Actions>;
  reducers: Pick<
    MakeContainerBuilderLogicType<EntryType>['reducers'],
    Reducers
  >;
}>;
