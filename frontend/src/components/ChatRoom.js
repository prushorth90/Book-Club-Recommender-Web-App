import React, { useState, useEffect } from "react";
import { useParams } from "react-router";
import axiosInstance from "../axios";
import { makeStyles } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';
import Button from "@material-ui/core/Button";
import moment from 'moment'

const MessageApi = {
    getMessages: (roomId) => axiosInstance.get('/messages', { params: { club_id: roomId } }),
    addMessage: (id, message, userId) => axiosInstance.post("/messages/", { 
        chat_room: userId,
        message: message, 
        created_by: id,
    })
}

const ClubApi = {
    getUsers: (clubId) => axiosInstance.get(`/member-list/${clubId}`),
    banUserFromChat: (userId, clubId) => axiosInstance.delete(`/chat-room/${clubId}/remove-user/${userId}`)
}


const useUserId = () => {
    const refreshToken = localStorage.getItem('access_token');
    const tokenParts = JSON.parse(atob(refreshToken.split('.')[1]));
    return tokenParts.user_id
}



const useStyles = makeStyles((theme) => ({
    main: {
        position: 'relative',
        height: '100vh',
        width: '100vw',
        // background: 'red'
    },
    messages: {
        position: 'absolute',
        left: 0,
        width: '80%',
        height: '100%',
        // background: 'green',
    },
    composer: {
        borderTop: '1px solid black',
        padding: '10px'
    },
    history: {
        height: "calc(100vh - 80px)",
        padding: "15px",
        overflowY: "auto"
    },
    sidebar: {
        position: 'absolute',
        right: 0,
        width: '20%',
        height: '100%',
        overflowY: "auto",
        borderLeft: "1px solid black",
    },
    sidebarInner: {
        padding: "15px"
    },
    myMessage: {
        padding: "8px",
        borderRadius: "5px",
        background: "#196DDC",
        color: "white",
        textAlign: "right",
        display: "inline-block",
        margin: "2px"
    },
    theirMessage: {
        padding: "8px",
        borderRadius: "5px",
        background: "#F1F2F4",
        color: "black",
        textAlign: "left",
        display: "inline-block",
        margin: "2px"
    },
    message: {
        display: "block"
    }
}));

const Message = ({ message, index }) => {
    const userId = useUserId();
    const styles = useStyles();
    const isMe = userId == message.created_by
  
    const cssClassTime = (isMe ? 'time-left' : 'time-right');
    return (
        <div className={styles.message} style={{textAlign: isMe ? "right" : "left"}}>
            <div className={isMe ? styles.myMessage : styles.theirMessage}>
                <div>
                    <p>{message.message}</p>
                    <span className={cssClassTime}>{message.username}</span>
                    <sub>{moment(message.timestamp).format("LLL")}</sub>
                </div>
            </div>
        </div>
    );
}

const AddMessage = (props) => {
    const userId = useUserId();
    const { id } = useParams
    
    
    const [message, setMessage] = useState('')
    console.log(userId)
    const submitMessage = () => {
        MessageApi.addMessage(id,message, userId);
        setMessage('');
    }
    return (
        <div className="footer">
            <TextField style={{width: "200px"}} placeholder="New Message" value={message} onChange={e => setMessage(e.target.value)} />
            <Button variant="contained" onClick={submitMessage}>Submit</Button >
        </div>

    )

}


export default function ChatRoom() {
    const { id } = useParams()
    const [messages, setMessages] = useState([])
    const styles = useStyles();
    console.log(id)
    useEffect(() => {
        MessageApi.getMessages(id)
            .then((res) => {
                setMessages(res.data)
            }
            )
        var feed = setInterval(() => {
            MessageApi.getMessages(id)
                .then((res) => {
                    setMessages(res.data)
                }
                )
        }, 1000)
        return () => clearInterval(feed)
    }, [id])

    return (
        <div className={styles.main}>
            <div className={styles.messages}>
                <div className={styles.history}>
                    {messages.map((message, index) => <Message message={message} index={index} />)}
                </div>
                <div className={styles.composer}>
                    <AddMessage id={id} />
                </div>
            </div>
            <div className={styles.sidebar}>
                <div className={styles.sidebarInner}>
                    <ClubMembers />
                </div>
            </div>
        </div>
    )
}

const ClubMembers = ({ onClose }) => {
    const { id } = useParams()
    const [users, setUsers] = useState(null);

    const banUser = (userId) => {
        ClubApi.banUserFromChat(userId, id);
    }

    useEffect(() => {
        ClubApi.getUsers(id).then(u => setUsers(u.data))
    }, [id])


    return <>
        {users ? users.length > 0 ? users.map(user => <div><strong>{user.user}</strong><button onClick={() => banUser(user.id)}>Ban</button></div>) : <p>No users found</p> : <p>Loading</p>}
    </>

}
