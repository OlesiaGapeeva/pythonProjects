import React from 'react';
import { Link } from 'react-router-dom'
import styles from './header.module.scss'

const Header: React.FC = () => {
    return (
        <div className={styles.header}>
        <div className={styles.header__wrapper}>
          <div className={styles.header__img}>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="50"
              height="50"
              fill="currentColor"
              viewBox="0 0 16 16"
            >
              <path d="M12.354 4.354a.5.5 0 0 0-.708-.708L5 10.293 1.854 7.146a.5.5 0 1 0-.708.708l3.5 3.5a.5.5 0 0 0 .708 0l7-7zm-4.208 7-.896-.897.707-.707.543.543 6.646-6.647a.5.5 0 0 1 .708.708l-7 7a.5.5 0 0 1-.708 0z"/>
              <path d="m5.354 7.146.896.897-.707.707-.897-.896a.5.5 0 1 1 .708-.708z"/>
            </svg>
            mm
          </div>
          <Link to='/vacancies' className={styles.header__logo}>Сервис по поиску вакансий</Link>
          <div className={styles.header__profileWrapper}>
            <Link to="/" className={styles.header__profile}>Корзина</Link>
            <span className={styles.header__spacer}>&nbsp;&nbsp;&nbsp;</span> {/* Увеличенный пробел */}
            <Link to="/" className={styles.header__profile}>Личный кабинет</Link>
          </div>
        </div>
      </div>
    )
};

export default Header;