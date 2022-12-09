import type { SelectorsDef } from '@/logic/types';
import { ApiErrorCodes, RequestStatus, ServiceErrorType } from '@/services';

import type { RoleUpdateLogic } from './type';

export const Selectors: SelectorsDef<RoleUpdateLogic> = () => ({
  saveStatus: [
    (selectors) => [selectors.createStatus],
    (createStatus) => createStatus,
  ],
  inputReady: [
    (selectors) => [
      selectors.selectedPermissions,
      selectors.name,
      selectors.isDefault,
    ],
    (_, name) => {
      return name.length > 4;
    },
  ],
  nameTooShort: [
    (selectors) => [selectors.name, selectors.saveClicked],
    (name, saveClicked) => {
      return saveClicked && name.length < 4;
    },
  ],
  nameTaken: [
    (selectors) => [selectors.createStatus, selectors.createError],
    (createStatus, createError) => {
      if (
        createError == null ||
        createError.type != ServiceErrorType.ApiError
      ) {
        return false;
      }
      return (
        createStatus == RequestStatus.Failure &&
        createError.detail == ApiErrorCodes.RoleNameTaken
      );
    },
  ],
});
