import { useInjection } from 'inversify-react';
import { useActions } from 'kea';
import { memo } from 'react';
import { RiLogoutBoxLine } from 'react-icons/ri';

import { IAuthLogic } from '@/logic/interfaces';

import { TopbarDialog } from '../dialog';
import { TopbarDialogItem } from '../dialogItem';
import './style.scss';

export const TopbarAvatarDialog = memo(function TopbarAvatarDialog() {
  const authLogic = useInjection(IAuthLogic.$);

  const { logout } = useActions(authLogic);

  return (
    <TopbarDialog>
      <TopbarDialogItem
        icon={RiLogoutBoxLine}
        title="logout"
        onClick={logout}
        iconSize="1.4rem"
      />
    </TopbarDialog>
  );
});
