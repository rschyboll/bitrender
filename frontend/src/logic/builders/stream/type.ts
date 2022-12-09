import type { MakeOwnLogicType } from '@/logic/types/';
import { RestrictedObject } from '@/types/utility';

import { StreamStatus } from './../../../services/enums';

export type Stream<
  ReceiveMessageType,
  StreamInput = unknown,
  SendMessageType = unknown,
> = (
  listeners: {
    onOpen: () => void;
    onMessage: (message: ReceiveMessageType) => void;
    onError: (error: Error) => void;
    onClose: () => void;
  },
  input: StreamInput,
) => {
  cancel: () => void;
  sendMessage: (message: SendMessageType) => void;
};

type StreamReceiveType<S> = S extends Stream<infer ReceiveType, any, any>
  ? ReceiveType
  : unknown;

type StreamSendType<S> = S extends Stream<any, any, infer SendType>
  ? SendType
  : unknown;

type StreamInputType<S> = S extends Stream<any, infer InputType, any>
  ? InputType
  : unknown;

export type StreamBuilderInput<
  Logic extends MakeOwnLogicType & MakeStreamBuilderLogicType,
> = Logic['__internal_stream_types'];

type Actions<Streams extends RestrictedObject<Streams, Stream<any, any, any>>> =
  {
    [Key in keyof Streams as Key extends string
      ? `${Key}StreamStart`
      : never]: unknown extends StreamInputType<Streams[Key]>
      ? () => void
      : (input: StreamInputType<Streams[Key]>) => { input: number };
  } & {
    [Key in keyof Streams as Key extends string
      ? `${Key}StreamStop`
      : never]: true;
  } & {
    [Key in keyof Streams as Key extends string
      ? `on${Capitalize<Key>}StreamOpen`
      : never]: (message: StreamReceiveType<Streams[Key]>) => {
      message: StreamReceiveType<Streams[Key]>;
    };
  } & {
    [Key in keyof Streams as Key extends string
      ? `on${Capitalize<Key>}StreamMessage`
      : never]: (message: StreamReceiveType<Streams[Key]>) => {
      message: StreamReceiveType<Streams[Key]>;
    };
  } & {
    [Key in keyof Streams as Key extends string
      ? `on${Capitalize<Key>}StreamError`
      : never]: (error: Error) => { error: Error };
  } & {
    [Key in keyof Streams as Key extends string
      ? `on${Capitalize<Key>}StreamClose`
      : never]: true;
  } & {
    [Key in keyof Streams as unknown extends StreamSendType<Streams[Key]>
      ? never
      : Key extends string
      ? `sendTo${Capitalize<Key>}Stream`
      : never]: (message: StreamSendType<Streams[Key]>) => {
      message: StreamSendType<Streams[Key]>;
    };
  } & {
    [Key in keyof Streams as unknown extends StreamSendType<Streams[Key]>
      ? never
      : Key extends string
      ? `sendTo${Capitalize<Key>}StreamSuccess`
      : never]: (message: StreamSendType<Streams[Key]>) => {
      message: StreamSendType<Streams[Key]>;
    };
  } & {
    [Key in keyof Streams as unknown extends StreamSendType<Streams[Key]>
      ? never
      : Key extends string
      ? `sendTo${Capitalize<Key>}StreamFailure`
      : never]: (message: StreamSendType<Streams[Key]>) => {
      message: StreamSendType<Streams[Key]>;
      error?: Error;
    };
  };

type Cache<Streams extends RestrictedObject<Streams, Stream<any, any, any>>> = {
  [Key in keyof Streams as Key extends string
    ? `cancel${Capitalize<Key>}Stream`
    : never]: true;
} & {
  [Key in keyof Streams as Key extends string
    ? `sendTo${Capitalize<Key>}Stream`
    : never]: true;
};

type Reducers<
  Streams extends RestrictedObject<Streams, Stream<any, any, any>>,
> = {
  [Key in keyof Streams as Key extends string
    ? `${Key}StreamStatus`
    : never]: StreamStatus;
};

export type MakeStreamBuilderLogicType<
  Streams extends RestrictedObject<
    Streams,
    Stream<any, any, any>
  > = RestrictedObject<{}, Stream<any, any, any>>,
> = MakeOwnLogicType<{
  actions: RestrictedObject<Actions<Streams>, (...args: any[]) => any>;
  reducers: RestrictedObject<Reducers<Streams>, any>;
  cache: RestrictedObject<Cache<Streams>, unknown>;
}> & { __internal_stream_types: { [Key in keyof Streams]: Streams[Key] } };
