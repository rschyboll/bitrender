import { interfaces } from "inversify";
import { LogicWrapper } from "kea";

import { MakeOwnLogicType } from "@/logic/types/makeLogic";

interface Actions {}

interface Values {}

export type IRolesTableLogic = LogicWrapper<
  MakeOwnLogicType<{
    actions: Actions;
    values: Values;
  }>
>;

export namespace IRolesTableLogic {
  export const $: interfaces.ServiceIdentifier<IRolesTableLogic> =
    Symbol("IRolesTableLogic");
}
