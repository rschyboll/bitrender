import { useInjection } from 'inversify-react';
import { useValues } from 'kea';
import { Skeleton } from 'primereact/skeleton';
import { memo, useMemo } from 'react';
import { Trans } from 'react-i18next';

import { Logo } from '@/components/logo';
import { IAppLogic } from '@/logic/interfaces';

import { SidebarItem } from '../item';
import { Group, filterVisibleItems, sidebarModel } from '../model';
import './style.scss';

export const SidebarMobile = memo(function SidebarMobile() {
  return (
    <div className="sidebar-mobile select-none">
      <Logo titleVisible={true} />
      <ul className="sidebar-container">
        {sidebarModel.map((groupModel) => {
          return <SidebarMobileGroup key={groupModel.title} {...groupModel} />;
        })}
      </ul>
    </div>
  );
});

type SidebarMobileGroupProps = Group;

const SidebarMobileGroup = memo(function SidebarMobileGroup(
  props: SidebarMobileGroupProps,
) {
  const appLogic = useInjection(IAppLogic.$);
  const { appReady, currentUser } = useValues(appLogic);

  const visibleItems = useMemo(
    () => filterVisibleItems(props.items, currentUser?.permissions),
    [currentUser, props.items],
  );

  if (visibleItems.length == 0) {
    return null;
  }

  return (
    <li className="sidebar-group">
      {!appReady || currentUser == null ? (
        <Skeleton className="sidebar-group-title-loading" />
      ) : (
        <span className="sidebar-group-title">
          <Trans>{props.title}</Trans>
        </span>
      )}
      <div className="sidebar-group-container">
        {props.items.map((item) => {
          if (visibleItems.includes(item)) {
            return <SidebarItem key={item.path} {...item} />;
          }
          return <div key={item.path} />;
        })}
      </div>
      {props.spacer && <div className="sidebar-spacer" />}
    </li>
  );
});
