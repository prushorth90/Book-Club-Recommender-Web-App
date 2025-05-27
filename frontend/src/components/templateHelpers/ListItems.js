import React, { useContext } from 'react';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import ListSubheader from '@mui/material/ListSubheader';
import DashboardIcon from '@mui/icons-material/Dashboard';
import AddIcon from '@mui/icons-material/Add';
import PeopleIcon from '@mui/icons-material/People';
import AssignmentIcon from '@mui/icons-material/Assignment';
import PercentIcon from '@mui/icons-material/Percent';

import AuthContext from '../../context/AuthContext'
import { useNavigate } from 'react-router-dom';

export const MainListItems = () => {
  const {user} = useContext( AuthContext );
  const navigate = useNavigate();

  const handleDashboard = (e) => {
    navigate('/dashboard');
  }

  const handleMyClubs = (e) => {
    navigate('/my_clubs');
  }

  const handleCreateClub = (e) => {
    navigate('/create');
  }

  const handleRateBooks = (e) => {
    navigate('/rate_books');
  }


  return (
    <React.Fragment>
      <ListItemButton onClick={handleDashboard}>
        <ListItemIcon>
          <DashboardIcon style={{color: '#7f4820'}}/>
        </ListItemIcon>
        <ListItemText primary="Dashboard"/>
      </ListItemButton>
      <ListItemButton onClick={handleMyClubs}>
        <ListItemIcon>
          <PeopleIcon  style={{color: '#7f4820'}}/>
        </ListItemIcon>
        <ListItemText primary="My Clubs"/>
      </ListItemButton>
      <ListItemButton onClick={handleCreateClub}>
        <ListItemIcon>
          <AddIcon  style={{color: '#7f4820'}}/>
        </ListItemIcon>
        <ListItemText primary="Create Club"/>
      </ListItemButton>
      <ListItemButton onClick={handleRateBooks}>
        <ListItemIcon>
          <PercentIcon  style={{color: '#7f4820'}}/>
        </ListItemIcon>
        <ListItemText primary="Rate Books"/>
      </ListItemButton>
    </React.Fragment>
  );
}
