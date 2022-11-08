import { UserView } from "@/schemas/user";

import { MRole } from "@/types/models";

import { IUserValidators } from "../interfaces";
import { JSONSchemaType, ValidateFunction, Validators } from "./base";

export class UserValidators extends Validators implements IUserValidators {
  userViewSchema: JSONSchemaType<UserView> = {
    type: "object",
    properties: {
      id: { type: "string", format: "uuid" },
      createdAt: { type: "string", format: "date-time" },
      modifiedAt: { type: "string", format: "date-time" },
      email: { type: "string", format: "email" },
      username: { type: "string" },
      role: { type: "string" },
      permissions: {
        type: "array",
        items: { type: "string", enum: Object.values(MRole.Permission) },
      },
    },
    required: [
      "id",
      "createdAt",
      "modifiedAt",
      "email",
      "username",
      "role",
      "permissions",
    ],
  };
  userViewValidator: ValidateFunction<UserView>;

  public mediumPasswordRegExp = new RegExp(
    "^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.{8,})"
  );
  public strongPasswordRegExp = new RegExp(
    "^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.{10,})"
  );
  userEmailSchema: JSONSchemaType<string> = {
    type: "string",
    format: "email",
  };
  userEmailValidator: ValidateFunction<string>;

  constructor() {
    super();
    this.userViewValidator = this.ajv.compile(this.userViewSchema);
    this.userEmailValidator = this.ajv.compile(this.userEmailSchema);
  }

  public validateUserView(response: unknown): response is UserView {
    return this.userViewValidator(response);
  }

  public validateUserPasswordStrength(password: string): boolean {
    return this.mediumPasswordRegExp.test(password);
  }

  public validateUserEmail(email: string): boolean {
    return this.userEmailValidator(email);
  }
}
