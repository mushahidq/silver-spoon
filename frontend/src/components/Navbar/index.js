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
                    <NavLink to='/about'>About Struts</NavLink>
                    <NavLink to='/contact'>Contact</NavLink>
                </NavMenu>
            </Nav>
        </>
    )
}

export default Navbar;