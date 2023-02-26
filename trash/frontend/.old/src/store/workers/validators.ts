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
      create_date: { type: "string" },
      active: { type: "boolean" },
      subtask_id: { type: "string", nullable: true },
      test_id: { type: "string", nullable: true },
      composite_task_id: { type: "string", nullable: true },
    },
    required: ["id", "name", "create_date", "active"],
  },
};

export const workersValidator = ajv.compile(workersSchema);
