import { useInjection } from 'inversify-react';
import { useMountedLogic } from 'kea';

import { ITestMultiLogicType, ITestSingleLogicType } from '@/logic/interfaces';

export const TestComponent = () => {
  const logicKeys = ['test1', 'test2', 'test3', 'test4', 'test5'];

  return (
    <div>
      {logicKeys.map((key) => {
        return <TestSingleComponent key={key} logicKey={key} />;
      })}
      <TestMultiComponent logicKeys={logicKeys} />
    </div>
  );
};

interface TestSingleComponentProps {
  logicKey: string;
}

const TestSingleComponent = (props: TestSingleComponentProps) => {
  const testSingleLogic = useInjection(ITestSingleLogicType.$);
  useMountedLogic(testSingleLogic({ key: props.logicKey }));

  return <div></div>;
};

interface TestMultiComponentProps {
  logicKeys: string[];
}

const TestMultiComponent = (props: TestMultiComponentProps) => {
  const testMultiLogic = useInjection(ITestMultiLogicType.$);
  useMountedLogic(testMultiLogic({ keys: props.logicKeys }));

  return <div></div>;
};
