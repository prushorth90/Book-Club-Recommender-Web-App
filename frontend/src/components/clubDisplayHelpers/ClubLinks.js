import * as React from 'react';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import { Link, useParams} from "react-router-dom";
import Parragraph from './Parragraph';
import { useNavigate } from 'react-router-dom';


export default function ClubLinks() {

  const { id } = useParams();
	const navigate = useNavigate();

  const handleCreatePost = (e) => {
    navigate('/create-post/'+ id);  
  }

  const handleGoShowMeeting = (e) => {
    navigate('/show_meeting/'+ id);
  }

  const handleGoChatRoom = (e) => {
    navigate('/club/'+ id +'/chat-room/');
  }

  const handleCreateMeeting = (e) => {
    navigate('/create_meeting/'+ id);
  }

  return (
    <React.Fragment>
      <Parragraph> Useful Club Links</Parragraph>
        <ListItemButton onClick={handleCreatePost}>
          <ListItemText primary="Create Post"/>
        </ListItemButton>
        <ListItemButton onClick={handleGoChatRoom}>
          <ListItemText primary="Chat Room"/>
        </ListItemButton>
        <ListItemButton onClick={handleCreateMeeting}>
          <ListItemText primary="Create Meeting"/>
        </ListItemButton>
    </React.Fragment>
  );
} 