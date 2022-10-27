import { interfaces } from 'inversify';

export type KeysMatching<T, V> = {
  [K in keyof T]-?: T[K] extends V ? K : never;
}[keyof T];

export type ArrayElementType<Type extends unknown[]> =
  Type extends (infer ElementType)[] ? ElementType : never;

export type RecordValueType<Type extends Record<string, unknown>> =
  Type extends Record<string, infer ValueType> ? ValueType : never;

export type ServiceTypeFromIdentifier<
  Identifier extends interfaces.ServiceIdentifier,
> = Exclude<Identifier, string | symbol> extends interfaces.ServiceIdentifier<
  infer Type
>
  ? Type
  : never;
