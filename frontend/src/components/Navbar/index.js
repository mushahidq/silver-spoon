import React from 'react';
import {
    Nav,
    NavLink,
    Bars,
    NavMenu,
    NavBtn,
    NavBtnLink,
} from './NavbarElements';

const Navbar = () => {
    return (
        <>
            <Nav>
                <Bars />

                <NavMenu>
                    <NavLink to='/' activeStyle>Home</NavLink>
                    <NavLink to='/about_struts'>About Struts</NavLink>
                    <NavLink to='/about_log4j'>About Log4J</NavLink>
                    <NavLink to='/contact'>Contact</NavLink>
                </NavMenu>
            </Nav>
        </>
    )
}

export default Navbar;