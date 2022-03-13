import { FaBars } from 'react-icons/fa';
import { NavLink as Link } from 'react-router-dom';
import styled from 'styled-components';

export const Nav = styled.nav`
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 1rem;
    background: #fff;
    box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.1);
`;

export const NavLink = styled(Link)`
    color: #000;
    text-decoration: none;
    font-size: 1.2rem;
    font-weight: bold;
    padding: 0.5rem 1rem;
    &:hover {
        color: #000;
        background: #f5f5f5;
    }
`;

export const Bars = styled(FaBars)`
    font-size: 2rem;
    cursor: pointer;
    &:hover {
        color: #000;
    }
`;

export const NavMenu = styled.div`
    display: flex;
    align-items: center;
    margin-right: 1rem;
`;

export const NavBtn = styled.nav`
  display: flex;
  align-items: center;
  margin-right: 24px;
  /* Third Nav */
  /* justify-content: flex-end;
  width: 100vw; */
  @media screen and (max-width: 768px) {
    display: none;
  }
`;
  
export const NavBtnLink = styled(Link)`
  border-radius: 4px;
  background: #808080;
  padding: 10px 22px;
  color: #000000;
  outline: none;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  text-decoration: none;
  /* Second Nav */
  margin-left: 24px;
  &:hover {
    transition: all 0.2s ease-in-out;
    background: #fff;
    color: #808080;
  }
`;