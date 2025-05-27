import React from "react";
import { makeStyles, Container, Card, CardActionArea, CardMedia, CardContent, Typography, CardActions, Button } from "@material-ui/core";
import { Link } from "react-router-dom";

const useStyles = makeStyles((theme) => ({
    card:{
        marginBottom:theme.spacing(3)
    },
}));




const PostInfo = (props) => {

    const { posts } = props;
    const classes = useStyles();

    if (!posts || posts.length === 0) return <p> No posts made yet!</p>;
    return (
        <React.Fragment>
    {posts.map((post) => {
    return ( <Card item key={post.user} className={classes.card}>
        <CardActionArea>
             <CardContent>
                 <Typography gutterBottom variant="h5"> {post.user} </Typography>
                 <Typography variant="body2"> text: {post.text} </Typography>
             </CardContent>
        </CardActionArea>
    </Card>
    );
    })}
    </React.Fragment>
    );
};

export default PostInfo;