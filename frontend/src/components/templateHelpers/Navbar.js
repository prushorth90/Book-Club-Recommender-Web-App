import React, { useState, useEffect, useContext } from "react";
import { makeStyles, AppBar, Toolbar, Typography, InputBase} from "@material-ui/core";
import { Search, Person, Cancel } from "@material-ui/icons"
import { alpha } from "@material-ui/core/styles";
import { Badge, Menu, MenuItem } from "@material-ui/core";
import MenuBookIcon from '@mui/icons-material/MenuBook';
import axiosInstance from "../../axios";
import { Link } from "react-router-dom";
import AuthContext from "../../context/AuthContext";

const useStyles = makeStyles((theme) => ({
    toolbar: {
        display:"flex",
        justifyContent:"space-between",

        backgroundColor: "#261509"
    },
    logoLg:{
        display: "none",
        [theme.breakpoints.up("sm")]: {
            display: "block",
        },
    },
    logoSm:{
        display: "block",
        [theme.breakpoints.up("sm")]: {
            display: "none",
    },
},
search:{
    display: "flex",
    alignItems: "center",
    backgroundColor: alpha(theme.palette.common.white, 0.15),
    '&:hover': {
      backgroundColor: alpha(theme.palette.common.white, 0.25),
    },
    borderRadius: theme.shape.borderRadius,
    width: "50%",
    [theme.breakpoints.down("sm")]: {
        display: (props) => (props.open ? "flex" : "none"),
        width: "70%",
    },
},
input:{
    color:"white",
    marginLeft: theme.spacing(1),
},
cancel: {
    [theme.breakpoints.up("sm")] : {
        display: "none",
    }
},
searchButton:{
    marginRight:theme.spacing(2),
    [theme.breakpoints.up("sm")]: {
        display: "none",
    },
},
icons:{
    alignItems: "center",
    display: (props) => (props.open ? "none" : "flex"),
    },
badges:{
    marginRight:theme.spacing(2),
},
}));

const Navbar = () => {
    let {user} = useContext(AuthContext)

    //get the logged in user data
    
    const [data, setData] = useState({ currentUser: [] });

    useEffect(() =>  {
        axiosInstance.get('current-user').then((res) => {
            setData({ currentUser: res.data });
          console.log(res.data);
        });
    }, [setData]);


    const [open, setOpen] = useState(false);
    const classes = useStyles({ open });

    const [anchorEl, setAnchorEl] = React.useState(null);

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

    return (
    <AppBar position="fixed">
        <Toolbar className={classes.toolbar}>
            <Typography variant="h6"  href='dashboard' >
                Bookaholics
            </Typography>
            <Typography variant="h6">
            </Typography>
            <div className={classes.icons}>
                <Search className={classes.searchButton} onClick={()=>setOpen(true)} />
                <Badge className={classes.badge} aria-controls="simple-menu" aria-haspopup="true" onClick={handleClick}>
                    <Person/>
                </Badge>
                <Menu
                    id="simple-menu"
                    anchorEl={anchorEl}
                    keepMounted
                    open={Boolean(anchorEl)}
                    onClose={handleClose}
                >
                    <Link to={"/update_profile"}>            
                        <MenuItem>Update Profile</MenuItem>
                    </Link>
                    <MenuItem component='a' href='update_password'>Change Password</MenuItem>
                    <MenuItem component='a' href='logout'>Logout</MenuItem>
                </Menu>
            </div>
        </Toolbar>
    </AppBar>
        
    );
    
};

export default Navbar;
/*
            <div className={classes.search}>
                <Search/>
                <InputBase placeholder="Search..." className={classes.input} />
                <Cancel className={classes.cancel} onClick={()=>setOpen(false)} />
            </div>*/