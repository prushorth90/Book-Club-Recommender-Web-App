import React, { useState, useEffect } from "react";
import { styled, createTheme, ThemeProvider } from '@mui/material/styles';
import MuiDrawer from '@mui/material/Drawer';
import Toolbar from '@mui/material/Toolbar';
import List from '@mui/material/List';
import Divider from '@mui/material/Divider';
import IconButton from '@mui/material/IconButton';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import { MainListItems } from './ListItems';
import { ClubListItems } from './ClubListItems';
import { ClubListOwner } from './ClubListOwner';

import { useParams } from 'react-router-dom';
import axiosInstance from '../../axios';

const drawerWidth = 240;

const Drawer = styled(MuiDrawer, { shouldForwardProp: (prop) => prop !== 'open' })(
  ({ theme, open }) => ({
    '& .MuiDrawer-paper': {
      position: 'fixed',
      top: 64,
      whiteSpace: 'nowrap',
      width: drawerWidth,
      transition: theme.transitions.create('width', {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.enteringScreen,
      }),
      boxSizing: 'border-box',
      ...(!open && {
        overflowX: 'hidden',
        transition: theme.transitions.create('width', {
          easing: theme.transitions.easing.sharp,
          duration: theme.transitions.duration.leavingScreen,
        }),
        width: theme.spacing(7),
        [theme.breakpoints.up('sm')]: {
          width: theme.spacing(9),
        },
      }),
    },
  }),
);

const mdTheme = createTheme();

function ClubDrawerContent() {
  const [open, setOpen] = React.useState(false);
  const toggleDrawer = () => {
    setOpen(!open);
  };

  const { id } = useParams();
  const [userAuth, setUserAuth] = useState(null);

  useEffect(() => {
    axiosInstance.get('user-auth-detail/' + id + '/')
    .then((response) => {
      setUserAuth(response.data.rank);
      })
    .catch((e) => {
      setUserAuth(e.response.data.detail);
    });
  }, [setUserAuth]);


  return (
    <ThemeProvider theme={mdTheme}>
        <Drawer variant="permanent" open={open} >
          <Toolbar
            sx={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'flex-end',
              px: [1],
            }}
          >
            <IconButton onClick={toggleDrawer}>
              <ChevronRightIcon />
            </IconButton>
          </Toolbar>
          <Divider />
          <List component="nav">
            <MainListItems />
            <Divider sx={{ my: 1 }} />
            <ClubListItems />
            {userAuth == 'owner' &&
              <ClubListOwner/>
            }
          </List>
        </Drawer>
    </ThemeProvider>
  );
}

export default function Dashboard() {
  return <ClubDrawerContent />;
}
