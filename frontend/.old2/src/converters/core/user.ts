import { injectable } from 'inversify';

import { IUserConverters } from '@/converters/interfaces';

@injectable()
export class UserConverters implements IUserConverters {}
