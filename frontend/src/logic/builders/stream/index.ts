import { LogicBuilder, actions, listeners, reducers } from 'kea';

import type { MakeOwnLogicType } from '@/logic';
import { StreamStatus } from '@/services';
import { capitalizeFirstLetter } from '@/utils/string';

import type {
  MakeStreamBuilderLogicType,
  Stream,
  StreamBuilderInput,
} from './type';

export * from './type';

export function container<
  Logic extends MakeOwnLogicType & MakeStreamBuilderLogicType,
>(
  input:
    | StreamBuilderInput<Logic>
    | ((logic: Logic) => StreamBuilderInput<Logic>),
): LogicBuilder<Logic> {
  return (logic) => {
    const streams = typeof input === 'function' ? input(logic) : input;

    for (const key in streams) {
      const keyCapitalized = capitalizeFirstLetter(key);
      const stream = streams[key] as Stream<unknown, unknown, unknown>;

      actions({
        [`${key}StreamStart`]: (input: unknown) => ({ input }),
        [`${key}StreamStop`]: true,
        [`on${keyCapitalized}StreamOpen`]: true,
        [`on${keyCapitalized}StreamMessage`]: (message: unknown) => ({
          message,
        }),
        [`on${keyCapitalized}StreamError`]: (error: unknown) => ({
          error,
        }),
        [`on${keyCapitalized}StreamClose`]: true,
      })(logic);

      reducers({
        [`${key}StreamStatus`]: [
          StreamStatus.Closed,
          {
            [`${key}StreamStart`]: () => StreamStatus.Connecting,
            [`${key}StreamStop`]: () => StreamStatus.Closing,
            [`on${keyCapitalized}StreamOpen`]: () => StreamStatus.Open,
            [`on${keyCapitalized}StreamClose`]: () => StreamStatus.Closed,
            [`on${keyCapitalized}StreamError`]: () => StreamStatus.Closed,
          },
        ],
      })(logic);

      listeners(
        ({
          cache,
          actions,
        }: MakeOwnLogicType<{
          actions: Record<string, (...args: any[]) => any>;
          cache: Record<string, any>;
        }>) => ({
          [`${key}StreamStart`]: (input: unknown) => {
            const onMessage = (message: unknown) => {
              actions[`on${keyCapitalized}StreamMessage`](message);
            };
            const onError = (error: Error) => {
              actions[`on${keyCapitalized}StreamError`](error);
            };
            const onClose = () => {
              actions[`on${keyCapitalized}StreamClose`]();
            };
            const onOpen = () => {
              actions[`on${keyCapitalized}StreamOpen`]();
            };

            const { cancel, sendMessage } = stream(
              {
                onOpen,
                onMessage,
                onError,
                onClose,
              },
              input,
            );

            cache[`cancel${keyCapitalized}Stream`] = cancel;
            cache[`sendTo${keyCapitalized}Stream`] = sendMessage;
          },
          [`${key}StreamStop`]: () => {
            cache[`cancel${keyCapitalized}Stream`]();
          },
          [`sendTo${keyCapitalized}Stream`]: (message: unknown) => {
            const sendTo = cache[`sendTo${keyCapitalized}Stream`];
            if (sendTo != null) {
              sendTo(message);
            }
          },
        }),
      );
    }

    return logic;
  };
}
