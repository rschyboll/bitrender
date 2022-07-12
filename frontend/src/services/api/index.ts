import { inject } from 'inversify';
import ky from 'ky';

import Dependencies from '@/deps';
import { IServiceValidators } from '@/validators/interfaces';

export class Service {
  protected api: typeof ky;
  protected serviceValidators: IServiceValidators;

  constructor() {
    this.api = ky.create({ prefixUrl: 'http://127.0.0.1:8000/api/app' });
    this.serviceValidators = Dependencies.get(IServiceValidators.$);
  }
}

export { UserService } from './user';
