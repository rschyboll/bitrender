import Ajv from 'ajv';
import addFormats from 'ajv-formats';
import { injectable } from 'inversify';

export { JSONSchemaType, ValidateFunction } from 'ajv';

@injectable()
export class Validators {
  protected ajv: Ajv;

  constructor() {
    this.ajv = new Ajv({});

    addFormats(this.ajv);
  }
}

export { UserValidators } from './user';
export { ServiceValidators } from './service';
