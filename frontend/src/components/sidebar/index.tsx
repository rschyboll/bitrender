import { FC, useState } from 'react';
import { useLocation } from 'react-router-dom';

import './style.scss';

export const Sidebar: FC = () => {
  const location = useLocation();

  return <div className="sidebar-static">{}</div>;
};
