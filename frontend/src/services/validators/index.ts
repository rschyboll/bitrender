import Ajv from 'ajv';
import addFormats from 'ajv-formats';

export { JSONSchemaType } from 'ajv';

export const ajv = new Ajv({});
addFormats(ajv);
