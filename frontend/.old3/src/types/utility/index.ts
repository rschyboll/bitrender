/* eslint-disable @typescript-eslint/ban-types */

/* eslint-disable @typescript-eslint/no-explicit-any */
import { interfaces } from 'inversify';

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

export type PartialRecord<K extends keyof any, T> = {
  [P in K]?: T;
};

export type RestrictedObject<O, AllowedTypes> = {
  [P in keyof O]: O[P] extends AllowedTypes
    ? O[P]
    : Record<string, never> extends AllowedTypes
    ? O[P] extends Record<string, unknown>
      ? RestrictedObject<O[P], AllowedTypes>
      : AllowedTypes
    : AllowedTypes;
};

export type Writeable<T> = { -readonly [P in keyof T]: T[P] };

export type PartialBy<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>;

export type RequiredBy<T, K extends keyof T> = Omit<T, K> &
  Required<Pick<T, K>>;

export type StringKeys<Interface> = Extract<keyof Interface, string>;

export type ChangeTypeOfKeys<
  T extends object,
  Keys extends keyof T,
  NewType,
> = {
  [key in keyof T]: key extends Keys ? NewType : T[key];
};

export type RecursiveChangeTypeOfKeys<T, OldType, NewType> = {
  [P in keyof T]: T[P] extends (infer U)[]
    ? RecursiveChangeTypeOfKeys<U, OldType, NewType>[]
    : T[P] extends OldType | undefined
    ? NewType
    : T[P] extends object | undefined
    ? RecursiveChangeTypeOfKeys<T[P], OldType, NewType>
    : T[P];
};

export type KeysMatching<T, V> = {
  [K in keyof T]-?: T[K] extends V ? K : never;
}[keyof T];

export type RemoveKeysWithType<Type, RemoveType> = {
  [Key in keyof Type as Type[Key] extends RemoveType ? never : Key]: Type[Key];
};

export type RecursiveRemoveKeysWithType<Type, RemoveType> = {
  [Key in keyof Type as Type[Key] extends RemoveType
    ? never
    : Key]: Type[Key] extends object
    ? RecursiveRemoveKeysWithType<Type[Key], RemoveType>
    : Type[Key];
};

export type ClassProperties<Class> = RecursiveRemoveKeysWithType<
  Class,
  Function
>;

export type KeepKeysWithType<Type, KeepType> = {
  [Key in keyof Type as Type[Key] extends KeepType ? Key : never]: Type[Key];
};

export type RecursivePartial<T> = {
  [P in keyof T]?: T[P] extends (infer U)[]
    ? RecursivePartial<U>[]
    : T[P] extends number | string | symbol | undefined
    ? T[P]
    : RecursivePartial<T[P]>;
};

export type ReplaceReturnType<T extends (...a: any) => any, TNewReturn> = (
  ...a: Parameters<T>
) => TNewReturn;

export type ChangeTypeOfSubKeys<
  T extends object,
  Key extends keyof T,
  SubKeys extends keyof T[Key],
  NewType,
> = {
  [key in keyof T]: key extends Key
    ? {
        [subkey in keyof T[Key]]: subkey extends SubKeys
          ? NewType
          : T[key][subkey];
      }
    : T[key];
};
export type Exactify<T, X extends T> = T & {
  [K in keyof X]: K extends keyof T ? X[K] : never;
};
