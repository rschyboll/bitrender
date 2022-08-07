import { injectable } from 'inversify';
import { Options } from 'ky';
import camelCase from 'lodash/camelCase';
import isArray from 'lodash/isArray';
import isObject from 'lodash/isObject';
import isPlainObject from 'lodash/isPlainObject';
import snakeCase from 'lodash/snakeCase';

export { UserConverters } from './user';

@injectable()
export class UtilityConverters {
  public uuidValidate(value: string) {
    const regex =
      /^(?:[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}|00000000-0000-0000-0000-000000000000)$/i;
    return regex.test(value);
  }

  public mapKeysDeep(
    object: unknown,
    keyConverter: (value: string) => string,
  ): unknown {
    if (isArray(object)) {
      return object.map((item: unknown) => {
        return this.mapKeysDeep(item, keyConverter);
      });
    }

    if (isPlainObject(object)) {
      return Object.keys(object as Record<string, unknown>).reduce(
        (accumulator: Record<string, unknown>, key: string) => {
          const value = (object as Record<string, unknown>)[key];
          const newKey = this.uuidValidate(key) ? key : keyConverter(key);
          accumulator[newKey] = isObject(value)
            ? this.mapKeysDeep(value, keyConverter)
            : value;
          return accumulator;
        },
        {},
      );
    }

    return object;
  }

  public async requestToSnakeCase(request: Request, options: Options) {
    if (options.body && !(options.body instanceof FormData)) {
      const body = JSON.parse(options.body as string);
      const convertedBody = this.mapKeysDeep(body, snakeCase);
      return new Request(request, { body: JSON.stringify(convertedBody) });
    }
  }

  public async responseToCamelCase(
    _: unknown,
    __: unknown,
    response: Response,
  ) {
    try {
      const body = await response.json();
      const convertedBody = this.mapKeysDeep(body, camelCase);
      return new Response(JSON.stringify(convertedBody), response);
    } catch (e) {
      return;
    }
  }
}
