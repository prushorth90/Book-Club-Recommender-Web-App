import React from 'react';
import Navbar from './templateHelpers/Navbar';
import DashboardContent from './templateHelpers/Drawer';
import ClubDrawerContent from './templateHelpers/ClubDrawer';

const Template = () => {
  return (
    <>
        <Navbar/>
        <DashboardContent/>
    </>
  )
}

export default Template