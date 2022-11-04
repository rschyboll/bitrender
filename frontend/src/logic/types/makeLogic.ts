/* eslint-disable @typescript-eslint/no-explicit-any, @typescript-eslint/ban-types*/
import {
  ActionCreatorForPayloadBuilder,
  ActionForPayloadBuilder,
  AnyFunction,
  ListenerFunction,
  Logic,
  PartialRecord,
  ReducerFunction,
} from 'kea';

import { RestrictedObject } from '@/types/utility';

type GetSelectorsValues<Selectors> = {
  [Key in keyof Selectors]: Selectors[Key] extends (
    ...args: any[]
  ) => infer ReturnType
    ? ReturnType
    : never;
};

type MakeActions<
  Actions,
  GenericActions extends
    | PartialRecord<keyof Actions, (...args: any[]) => void>
    | undefined,
> = {
  [ActionKey in keyof Actions]: ActionKey extends keyof GenericActions
    ? unknown extends GenericActions[ActionKey]
      ? Actions[ActionKey] extends AnyFunction
        ? ActionForPayloadBuilder<Actions[ActionKey]>
        : never
      : GenericActions[ActionKey]
    : Actions[ActionKey];
};

export interface MakeOwnLogicType<
  LogicData extends {
    actions?: RestrictedObject<
      LogicData['actions'],
      ((...args: any[]) => any) | true
    >;
    reducers?: RestrictedObject<LogicData['reducers'], any>;
    selectors?: RestrictedObject<
      LogicData['selectors'],
      (...args: any[]) => any
    >;
    values?: RestrictedObject<LogicData['values'], any>;
    props?: RestrictedObject<LogicData['props'], any>;
    deps?: RestrictedObject<LogicData['deps'], any>;
    genericActions?: {
      [Key in keyof LogicData['actions']]?: Key extends keyof LogicData['genericActions']
        ? LogicData['actions'][Key] extends (...args: infer ActionArgs) => any
          ? LogicData['genericActions'][Key] extends (
              ...args: infer GenericArgs
            ) => void
            ? ActionArgs extends GenericArgs
              ? LogicData['genericActions'][Key]
              : never
            : never
          : never
        : never;
    };
    sharedListeners?: RestrictedObject<
      LogicData['sharedListeners'],
      () => void | Promise<void>
    >;
  } = any,
> extends Logic {
  actions: LogicData extends {
    actions: RestrictedObject<
      LogicData['actions'],
      ((...args: any[]) => any) | true
    >;
  }
    ? MakeActions<LogicData['actions'], LogicData['genericActions']>
    : Record<never, never>;
  actionKeys: Record<string, string>;
  actionTypes: { [ActionKey in keyof LogicData['actions']]: string };
  actionCreators: {
    [ActionKey in keyof LogicData['actions']]: LogicData['actions'][ActionKey] extends AnyFunction
      ? ActionCreatorForPayloadBuilder<LogicData['actions'][ActionKey]>
      : never;
  };
  reducers: {
    [Key in keyof LogicData['reducers']]: ReducerFunction<
      LogicData['reducers'][Key]
    >;
  };
  reducer: unknown extends LogicData['reducers']
    ? ReducerFunction
    : ReducerFunction<LogicData['reducers']>;
  selector: (
    state: any,
    props: LogicData['props'],
  ) => GetSelectorsValues<LogicData['selectors']>;
  sharedListeners: {
    [Key in keyof Logic['sharedListeners']]: ListenerFunction;
  };
  selectors: {
    [Key in keyof LogicData['reducers']]: (
      ...args: any[]
    ) => LogicData['reducers'][Key];
  } & RestrictedObject<LogicData['selectors'], (...args: any[]) => any>;
  defaults: {
    [Key in keyof LogicData['reducers']]: LogicData['reducers'][Key];
  };
  values: (LogicData extends {
    values: RestrictedObject<LogicData['values'], any>;
  }
    ? LogicData['values']
    : {}) &
    LogicData['reducers'] &
    GetSelectorsValues<LogicData['selectors']>;
  props: LogicData['props'];
  deps: LogicData['deps'];
  __internal_selector_types: LogicData['selectors'];
}
