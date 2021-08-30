import Ajv, { JSONSchemaType } from "ajv";

import { BinaryData } from "./types";

const ajv = new Ajv();

const binariesSchema: JSONSchemaType<BinaryData[]> = {
  type: "array",
  items: {
    type: "object",
    properties: {
      id: { type: "string" },
      url: { type: "string" },
      version: { type: "string" },
    },
    required: ["id", "url", "version"],
  },
};

export const binariesValidator = ajv.compile(binariesSchema);
