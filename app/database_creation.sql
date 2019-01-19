
CREATE DATABASE catering_db;

USE catering_db;

show tables;


drop table availableMenu;


CREATE TABLE availableMenu (
  event_code INT NOT NULL,
  submenu VARCHAR(30) NOT NULL,
  dish VARCHAR(200) NOT NULL,
  dish_desc VARCHAR(200) NOT NULL,
  image_path VARCHAR(200)   ,
  PRIMARY KEY (event_code,submenu,dish)
  );
  
  

select * from availableMenu;



CREATE TABLE menuvote (
  voter VARCHAR(30) NOT NULL,
  event_code INT NOT NULL,
  submenu VARCHAR(30) NOT NULL,
  item VARCHAR(30) NOT NULL,
  PRIMARY KEY (event_code,voter,submenu,item)
);


  
  
  CREATE TABLE SubmitedMenu (
  event_code INT NOT NULL,
  course VARCHAR(30) NOT NULL,
  dish VARCHAR(30) NOT NULL,
  dish_desc VARCHAR(30) NOT NULL,
  max_choises  INT NOT NULL,
  PRIMARY KEY (event_code)
  );
  
  
  
INSERT INTO availableMenu 
    (event_code, submenu,item) 
VALUES 
    (45215,'entre','ΞΙΦΙΑΣ Carpaccio'),
	(45215,'entre','ΧΤΑΠΟΔΙ'),
	(45215,'entre','ΠΡΙΝ ΤΗ ΝΗΣΤΕΙΑ'),
    (45215,'main','Μοσχαρι με Πορτοκάλι'),
	(45215,'main', 'Σφυρίδα στο Λαδόχαρτο'),
    (45215,'dessert', 'Εκμεκ'),
    (45215,'dessert', 'Πανακότα')
    ;


INSERT INTO availableMenu 
    (event_code, submenu,item) 
VALUES 
    (1234,'entre','Γαρίδες Σαγανάκι'),
	(1234,'entre','Μύδια Αχνιστά'),
	(1234,'entre','Ψητά Λαχανικά'),
    (1234,'main','T-bone Stake'),
	(1234,'main', 'Αρνάκι με τρούφα'),
    (1234,'dessert', 'Παγωτό'),
    (1234,'dessert', 'Τσιζ Κέικ')
    ;


INSERT INTO availableMenu 
    (event_code, submenu,item) 
VALUES 
    (1234,'drinks','Bordeuax'),
	(1234,'drinks','Amstel'),
	(1234,'drinks','Heineken');
    

    
    select * from availableMenu;
    