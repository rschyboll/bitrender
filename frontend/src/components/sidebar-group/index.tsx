import { Children, FC } from 'react';

export interface SidebarGroupProps {
  key: string;
  children: JSX.Element | JSX.Element[];
  title: string;
  icon: string;
  open: boolean;
  onOpen: (key: string) => void;
}

export const SidebarGroup: FC<SidebarGroupProps> = (props) => {
  return <div className="sidebar-group">{props.children}</div>;
};
