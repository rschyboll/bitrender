import Ajv, { JSONSchemaType } from "ajv";

import { TaskData } from "./types";

const ajv = new Ajv();

const tasksSchema: JSONSchemaType<TaskData[]> = {
  type: "array",
  items: {
    type: "object",
    properties: {
      id: { type: "string" },
      name: { type: "string" },
      samples: { type: "integer" },
      start_frame: { type: "integer" },
      end_frame: { type: "integer" },
      resolution_x: { type: "integer" },
      resolution_y: { type: "integer" },
      finished: { type: "boolean" },
      packed: { type: "boolean" },
    },
    required: [
      "id",
      "name",
      "samples",
      "start_frame",
      "end_frame",
      "resolution_x",
      "resolution_y",
      "finished",
      "packed",
    ],
  },
};

export const tasksValidator = ajv.compile(tasksSchema);
