import { LogicBuilder, actions, listeners, reducers } from 'kea';

import type { MakeOwnLogicType } from '@/logic/types/';
import { ErrorResponse, RequestStatus, Response } from '@/services';
import type { RestrictedObject } from '@/types/utility';

type RequestOutput<Request> = Request extends (
  ...args: any[]
) => Promise<Response<infer ReturnValue>>
  ? ReturnValue
  : never;

type RequestInput<Request> = Request extends (
  ...args: infer Args
) => Promise<Response<unknown>>
  ? Args
  : never;

export type RequestsBuilderInput<
  Logic extends MakeOwnLogicType<{
    actions: Record<string, (...args: any[]) => any>;
  }>,
> = {
  [Key in keyof Logic['actions'] as Key extends string
    ?
        | `${Key}`
        | `${Key}Success`
        | `${Key}Failure` extends keyof Logic['actions']
      ? Key
      : never
    : never]?: (
    input: Parameters<Logic['actions'][Key]>[0],
  ) => Key extends string
    ? Promise<
        Response<
          ReturnType<
            Logic['actionCreators'][`${Key}Success`]
          >['payload']['value']
        >
      >
    : never;
};

export type MakeRequestsBuilderLogicType<
  Requests extends RestrictedObject<
    Requests,
    (...args: any[]) => Promise<Response<unknown>>
  >,
> = MakeOwnLogicType<{
  reducers: RestrictedObject<
    {
      [Key in keyof Requests as Key extends string
        ? `${Key}Status`
        : never]: RequestStatus;
    } & {
      [Key in keyof Requests as Key extends string ? `${Key}Error` : never]:
        | ErrorResponse['error']
        | null;
    },
    any
  >;
  actions: {
    [Key in keyof Requests]: RequestInput<Requests[Key]>[0] extends undefined
      ? () => void
      : (input: RequestInput<Requests[Key]>[0]) => {
          input: RequestInput<Requests[Key]>[0];
        };
  } & {
    [Key in keyof Requests as Key extends string ? `${Key}Success` : never]: (
      result: RequestOutput<Requests[Key]>,
    ) => { value: RequestOutput<Requests[Key]> };
  } & {
    [Key in keyof Requests as Key extends string ? `${Key}Failure` : never]: (
      error?: ErrorResponse['error'],
    ) => { error?: ErrorResponse['error'] };
  };
}>;

export function requests<Logic extends MakeOwnLogicType>(
  input:
    | RequestsBuilderInput<Logic>
    | ((logic: Logic) => RequestsBuilderInput<Logic>),
): LogicBuilder<Logic> {
  return (logic) => {
    const requests = typeof input === 'function' ? input(logic) : input;
    for (const requestKey in requests) {
      const request = requests[requestKey];
      if (request == null) {
        break;
      }
      actions({
        [`${requestKey}`]: (input: any) => ({ input: input }),
        [`${requestKey}Success`]: (value: unknown) => ({ value }),
        [`${requestKey}Failure`]: (error?: unknown) => ({
          error,
        }),
      })(logic);

      listeners(
        ({
          actions,
        }: MakeOwnLogicType<{
          actions: Record<string, (...args: any) => any>;
        }>) => ({
          [requestKey]: async (payload: { input: any }) => {
            const response = await request(payload.input);
            if (response.success) {
              actions[`${requestKey}Success`](response.data);
            } else {
              actions[`${requestKey}Failure`](response.error);
            }
          },
        }),
      )(logic);

      reducers({
        [`${requestKey}Status`]: [
          RequestStatus.Idle,
          {
            [`${requestKey}`]: () => RequestStatus.Running,
            [`${requestKey}Success`]: () => RequestStatus.Success,
            [`${requestKey}Failure`]: () => RequestStatus.Failure,
          },
        ],
        [`${requestKey}Error`]: [
          null,
          {
            [`${requestKey}`]: () => null,
            [`${requestKey}Success`]: () => null,
            [`${requestKey}Failure`]: (
              _: unknown,
              { error }: { error?: ErrorResponse['error'] },
            ) => (error == null ? null : error),
          },
        ],
      })(logic);
    }
    return logic;
  };
}
