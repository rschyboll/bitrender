import Ajv, { JSONSchemaType } from "ajv";
import addFormats from "ajv-formats";

import { WorkerData } from "./types";

const ajv = new Ajv();
addFormats(ajv);

const workersSchema: JSONSchemaType<WorkerData[]> = {
  type: "array",
  items: {
    type: "object",
    properties: {
      id: { type: "string" },
      name: { type: "string" },
      register_date: { type: "string" },
      active: { type: "boolean" },
      test_time: { type: "number", nullable: true },
    },
    required: ["id", "name", "register_date", "active"],
  },
};

export const workersValidator = ajv.compile(workersSchema);
