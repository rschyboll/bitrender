import { injectable } from 'inversify';
import camelCase from 'lodash/camelCase';
import isArray from 'lodash/isArray';
import isObject from 'lodash/isObject';
import isPlainObject from 'lodash/isPlainObject';
import kebabCase from 'lodash/kebabCase';
import snakeCase from 'lodash/snakeCase';

import { UserView, UserViewResponse } from '@/types/user';

export { UserConverters } from './user';

@injectable()
export class UtilityConverters {
  public userViewResponseToUserView(viewResponse: UserViewResponse): UserView {
    return {
      ...viewResponse,
      modifiedAt: new Date(viewResponse.modified_at),
      createdAt: new Date(viewResponse.created_at),
    };
  }

  public camelCaseKeysToSnakeCase(o: unknown): unknown {
    if (this.isObject(o)) {
      const n: Record<string, unknown> = {};

      Object.keys(o).forEach((k) => {
        n[this.camelCaseKeyToSnakeCase(k)] = this.camelCaseKeysToSnakeCase(
          o[k],
        );
      });

      return n;
    } else if (this.isArray(o)) {
      return o.map((i) => {
        return this.camelCaseKeysToSnakeCase(i);
      });
    }

    return o;
  }

  public snakeCaseKeysToCamelCase(o: unknown): unknown {
    if (this.isObject(o)) {
      const n: Record<string, unknown> = {};

      Object.keys(o).forEach((k) => {
        n[this.snakeCaseKeyToCamelCase(k)] = this.snakeCaseKeysToCamelCase(
          o[k],
        );
      });

      return n;
    } else if (this.isArray(o)) {
      return o.map((i) => {
        return this.snakeCaseKeysToCamelCase(i);
      });
    }

    return o;
  }

  public camelCaseKeyToSnakeCase(s: string) {
    const result = s.replace(/([A-Z])/g, ' $1');

    return result.split(' ').join('_').toLowerCase();
  }

  public snakeCaseKeyToCamelCase(s: string) {
    return s.replace(/([-_][a-z])/gi, ($1) => {
      return $1.toUpperCase().replace('-', '').replace('_', '');
    });
  }

  public isObject(o: unknown): o is Record<string, unknown> {
    return o === Object(o) && !this.isArray(o) && typeof o !== 'function';
  }

  public isArray(a: unknown): a is unknown[] {
    return Array.isArray(a);
  }
}

const uuidValidate = function (value) {
  const regex =
    /^(?:[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}|00000000-0000-0000-0000-000000000000)$/i;
  return regex.test(value);
};

const mapKeysDeep = function (obj, fn) {
  if (isArray(obj)) {
    return obj.map((item) => {
      return mapKeysDeep(item, fn);
    });
  }

  if (isPlainObject(obj)) {
    return Object.keys(obj).reduce((accumulator, key) => {
      const value = obj[key];
      const newKey = uuidValidate(key) ? key : fn(key);
      accumulator[newKey] = isObject(value) ? mapKeysDeep(value, fn) : value;
      return accumulator;
    }, {});
  }

  return obj;
};

function createRequestModify(modifier) {
  return async (request, options) => {
    if (options.body && !(options.body instanceof FormData)) {
      const body = JSON.parse(options.body);
      const convertedBody = mapKeysDeep(body, modifier);
      return new Request(request, { body: JSON.stringify(convertedBody) });
    }
  };
}

function createResponseModify(modifier) {
  return async (input, options, response) => {
    try {
      const body = await response.json();
      const convertedBody = mapKeysDeep(body, modifier);
      return new Response(JSON.stringify(convertedBody), response);
    } catch (e) {
      return;
    }
  };
}

export const requestToSnakeCase = createRequestModify(snakeCase);
export const requestToCamelCase = createRequestModify(camelCase);
export const requestToKebabCase = createRequestModify(kebabCase);

export const responseToSnakeCase = createResponseModify(snakeCase);
export const responseToCamelCase = createResponseModify(camelCase);
export const responseToKebabCase = createResponseModify(kebabCase);
