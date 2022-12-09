import type { LogicWrapper } from 'kea';

import type { MakeOwnLogicType } from '../types';

export function delayLogicUnmount(
  logic: LogicWrapper<MakeOwnLogicType>,
  delay: number,
) {
  let mountCounter = 0;

  const oldBuild = logic.build;

  logic.build = (props) => {
    const buildLogic = oldBuild(props);

    buildLogic.wrapper = 1;
    buildLogic.mount = 1;
    console.log(buildLogic);
    buildLogic.unmount = () => {
      console.log('TEST');
    };

    return buildLogic;
  };
  logic.mount = 1;
  logic.unmount = () => {
    console.log('TEST');
  };

  return logic;
}
