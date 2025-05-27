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
import { useParams } from 'react-router-dom';



export const ClubListOwner = () => {
    const { id } = useParams();
    const navigate = useNavigate();
  
    const handleMembersList = (e) => {
      navigate('/member_list/' + id);
    }
  
    const handleapplicantList = (e) => {
      navigate('/applicant_list/'+ id);
    }
  
    return (
    <React.Fragment>
      <ListItemButton>
        <ListItemIcon>
          <AssignmentIcon  style={{color: '#7f4820'}}/>
        </ListItemIcon>
        <ListItemText primary="Members List" onClick={handleMembersList}/>
      </ListItemButton>
      <ListItemButton>
        <ListItemIcon>
          <AssignmentIcon style={{color: '#7f4820'}}/>
        </ListItemIcon>
        <ListItemText primary="Applicant List" onClick={handleapplicantList}/>
      </ListItemButton>
    </React.Fragment>
    )
  };