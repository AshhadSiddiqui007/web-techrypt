import React from 'react';
import { useIsMobile } from '../../hooks/useIsMobile';
import HeaderComponent from './Header';
import Mobilenav from './Mobilenav';

export default function HeaderWrapper() {
  const isMobile = useIsMobile();
  return isMobile ? <Mobilenav /> : <HeaderComponent />;
}