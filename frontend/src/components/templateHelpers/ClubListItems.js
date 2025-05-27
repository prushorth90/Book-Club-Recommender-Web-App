import React, { useContext } from 'react';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import ListSubheader from '@mui/material/ListSubheader';
import AssignmentIcon from '@mui/icons-material/Assignment';
import { useNavigate } from 'react-router-dom';
import { useParams } from 'react-router-dom';



export const ClubListItems = () => {
    const { id } = useParams();
    const navigate = useNavigate();
  
    const handleMembersList = (e) => {
      navigate('/member_list/' + id);
    }
  
    const handleGoShowMeeting = (e) => {
      navigate('/show_meeting/'+ id);
    }
  
    return (
    <React.Fragment>
      <ListSubheader component="div" inset>
        Club actions
      </ListSubheader>
      <ListItemButton>
        <ListItemIcon>
          <AssignmentIcon style={{color: '#7f4820'}}/>
        </ListItemIcon>
        <ListItemText primary="Show Meeting" onClick={handleGoShowMeeting}/>
      </ListItemButton>
    </React.Fragment>
    )
  };