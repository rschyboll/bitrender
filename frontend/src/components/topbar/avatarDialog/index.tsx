import { memo } from 'react';

import { TopbarDialog } from '../dialog';
import { TopbarDialogItem } from '../dialogItem';
import './style.scss';

export const TopbarAvatarDialog = memo(function TopbarAvatarDialog() {
  return (
    <TopbarDialog>
      <TopbarDialogItem />
      <TopbarDialogItem />
      <TopbarDialogItem />
      <TopbarDialogItem />
      <TopbarDialogItem />
    </TopbarDialog>
  );
});
