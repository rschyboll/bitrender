import { Logic, LogicWrapper } from 'kea';

export type RemoveDepsType<MyLogic extends LogicWrapper<Logic>> =
  MyLogic extends LogicWrapper<infer LogicType>
    ? LogicWrapper<{
        [Key in keyof LogicType]: 'props' extends Key
          ? Omit<LogicType['props'], 'deps'>
          : LogicType[Key];
      }>
    : never;

export function injectDepsToLogic<TWrappedLogic extends LogicWrapper<Logic>>(
  logic: TWrappedLogic,
  depsBuilder: () => TWrappedLogic['props']['deps'],
): RemoveDepsType<TWrappedLogic> {
  const oldBuild = logic.build;
  logic.build = (props: any) => {
    return oldBuild({ ...props, deps: depsBuilder() });
  };

  return logic as RemoveDepsType<TWrappedLogic>;
}
