-- drop objects
drop table ar_urnik cascade constraints;
drop table ar_gu_termin cascade constraints;
drop table ar_gov_ure cascade constraints;
drop table ar_skup_stud cascade constraints;
drop table ar_skupina cascade constraints;
drop table ar_prof_pred cascade constraints;
drop table ar_predmet_program cascade constraints;
drop table ar_namen cascade constraints;
drop table ar_profesor cascade constraints;
drop table ar_student cascade constraints;
drop table ar_predmet cascade constraints;
drop table ar_tip_dogodka cascade constraints;
drop table ar_sprogram cascade constraints;
drop table ar_prostor cascade constraints;
drop table ar_koledar cascade constraints;

-- create tables

create table ar_prostor (
    id            number generated by default on null as identity
                  constraint ar_prostor_id_pk primary key,
    naziv         varchar2(50 char),
    kapaciteta    number,
    vrsta         varchar2(20 char)
);



create table ar_sprogram (
    id                        number generated by default on null as identity
                              constraint ar_sprogram_id_pk primary key,
    naziv_programa            varchar2(150 char),
    strokovni_naziv           varchar2(150 char),
    stopnja                   varchar2(10 char) constraint ar_sprogram_stopnja_ck
                              check (stopnja in ('VS','UN','MAG','DR')),
    klasius_srv               varchar2(20 char),
    klasius_p16               varchar2(20 char),
    veljavnost_zac    date,
    veljavnost_kon    date
);



create table ar_predmet (
    id            number generated by default on null as identity
                  constraint ar_predmet_id_pk primary key,
    sifra         varchar2(9 char),
    naziv         varchar2(100 char),
    ects          number,
    ure_pred      number,
    ure_epred     number,
    ure_vaj       number,
    ure_evaj      number,
    ure_labvaj    number,
    ind_z_prof    number,
    sam_delo      number,
    vrsta         varchar2(10 char) constraint ar_predmet_vrsta_ck
                  check (vrsta in ('program','k.o.o.d.'))
);



create table ar_student (
    id               number generated by default on null as identity
                     constraint ar_student_id_pk primary key,
    sprogram         number
                     constraint ar_student_sprogram_fk
                     references ar_sprogram,
    ime              varchar2(30 char),
    priimek          varchar2(30 char),
    vpisna           number,
    identiteta       number,
    email            varchar2(50 char),
    letnik           varchar2(3 char) constraint ar_student_letnik_ck
                     check (letnik in ('1','2','3','ABS','X')),
    leto_prv_vpis    date,
    zac_datum        date,
    kon_datum        date,
	vrsta_vpisa      varchar2(3 char) constraint ar_student_vpis_ck
                     check (vrsta_vpisa in ('red','izr','obč')),
	ponavlja         varchar2(1) constraint ar_student_pon_ck
                     check (ponavlja in ('D','N'))
);

-- table index
create index ar_student_i1 on ar_student (sprogram);



create table ar_profesor (
    id            number generated by default on null as identity
                  constraint ar_profesor_id_pk primary key,
    prostor_id    number
                  constraint ar_profesor_prostor_id_fk
                  references ar_prostor,
    ime           varchar2(30 char),
    priimek       varchar2(30 char),
    naziv         varchar2(35 char),
    email         varchar2(50 char)
);

-- table index
create index ar_profesor_i1 on ar_profesor (prostor_id);



create table ar_namen (
    id                number generated by default on null as identity
                      constraint ar_namen_id_pk primary key,
    opis              varchar2(30 char),
    trajanje_minut    number
);



create table ar_tip_dogodka (
    id      number generated by default on null as identity
            constraint ar_tip_dogodka_id_pk primary key,
    opis    varchar2(25 char)
);



create table ar_predmet_program (
    id            number generated by default on null as identity
                  constraint ar_predmet_program_id_pk primary key,
    predmet_id    number
                  constraint ar_predmet_program_predmet_id_fk
                  references ar_predmet,
    program_id    number
                  constraint ar_predmet_program_program_id_fk
                  references ar_sprogram,
    letnik        number,
    obv_izb       varchar2(10 char) constraint ar_predmet_program_obv_izb_ck
                  check (obv_izb in ('obvezni','izbirni')),
    semester      varchar2(10 char) constraint ar_predmet_program_semester_ck
                  check (semester in ('zimski','poletni'))
);

-- table index
create index ar_predmet_program_i1 on ar_predmet_program (predmet_id);

create index ar_predmet_program_i2 on ar_predmet_program (program_id);



create table ar_prof_pred (
    id             number generated by default on null as identity
                   constraint ar_prof_pred_id_pk primary key,
    profesor_id    number
                   constraint ar_prof_pred_profesor_id_fk
                   references ar_profesor,
    predmet_id     number
                   constraint ar_prof_pred_predmet_id_fk
                   references ar_predmet,
    zac_datum      date,
    kon_datum      date
);

-- table index
create index ar_prof_pred_i1 on ar_prof_pred (profesor_id);

create index ar_prof_pred_i2 on ar_prof_pred (predmet_id);



create table ar_skupina (
    id       number generated by default on null as identity
             constraint ar_skupina_id_pk primary key,
    naziv    varchar2(150 char)
);



create table ar_skup_stud (
    id            number generated by default on null as identity
                  constraint ar_skup_stud_id_pk primary key,
    skupina_id    number
                  constraint ar_skup_stud_skupina_id_fk
                  references ar_skupina,
    student_id    number
                  constraint ar_skup_stud_student_id_fk
                  references ar_student,
    zac_datum     date,
    kon_datum     date,
    vloga         varchar2(20 char) constraint ar_skup_stud_vloga_ck
                  check (vloga in ('udeleženec','član','predsednik'))
);

-- table index
create index ar_skup_stud_i1 on ar_skup_stud (skupina_id);

create index ar_skup_stud_i2 on ar_skup_stud (student_id);



create table ar_gov_ure (
    id             number generated by default on null as identity
                   constraint ar_gov_ure_id_pk primary key,
    prostor_id     number
                   constraint ar_gov_ure_prostor_id_fk
                   references ar_prostor,
    profesor_id    number
                   constraint ar_gov_ure_profesor_id_fk
                   references ar_profesor,
    zac_datum      date,
    kon_datum      date,
    modif_datum    date,
    status_gu      varchar2(50 char),
    url            varchar2(255 char)
);

-- table index
create index ar_gov_ure_i1 on ar_gov_ure (prostor_id);

create index ar_gov_ure_i2 on ar_gov_ure (profesor_id);



create table ar_gu_termin (
    id              number generated by default on null as identity
                    constraint ar_gu_termin_id_pk primary key,
    govorilne_id    number
                    constraint ar_gu_termin_govorilne_id_fk
                    references ar_gov_ure,
    student_id      number
                    constraint ar_gu_termin_student_id_fk
                    references ar_student,
    namen_id        number
                    constraint ar_gu_termin_namen_id_fk
                    references ar_namen,
    zac_datum       date,
    kon_datum       date,
    modif_datum     date,
    status_gu       varchar2(50 char)
);

-- table index
create index ar_gu_termin_i1 on ar_gu_termin (govorilne_id);

create index ar_gu_termin_i2 on ar_gu_termin (student_id);

create index ar_gu_termin_i3 on ar_gu_termin (namen_id);



create table ar_urnik (
    id                number generated by default on null as identity
                      constraint ar_urnik_id_pk primary key,
    prostor_id        number
                      constraint ar_urnik_prostor_id_fk
                      references ar_prostor,
    profesor_id       number
                      constraint ar_urnik_profesor_id_fk
                      references ar_profesor,
    skupina_id        number
                      constraint ar_urnik_skupina_id_fk
                      references ar_skupina,
    predmet_id        number
                      constraint ar_urnik_predmet_id_fk
                      references ar_predmet,
    tip_dogodka_id    number
                      constraint ar_urnik_tip_dogodka_id_fk
                      references ar_tip_dogodka,
    zac_datum         date,
    kon_datum         date,
    komentar          varchar2(200 char),
    url               varchar2(255 char)
);

-- table index
create index ar_urnik_i1 on ar_urnik (prostor_id);

create index ar_urnik_i2 on ar_urnik (profesor_id);

create index ar_urnik_i3 on ar_urnik (skupina_id);

create index ar_urnik_i4 on ar_urnik (predmet_id);

create index ar_urnik_i5 on ar_urnik (tip_dogodka_id);



create table ar_koledar (
    id             number generated by default on null as identity
                   constraint ar_koledar_id_pk primary key,
    akad_datum     date,
    akad_status    varchar2(1 char) constraint ar_koledar_akad_status_ck
                   check (akad_status in ('D','N'))
);



-- Generated by Quick SQL undefined 24. 4. 2024, 11:28:08

/*
ar_prostor
  naziv vc50
  kapaciteta num
  vrsta vc20
ar_sprogram
  naziv_programa vc150
  strokovni_naziv vc150
  stopnja vc10 /check 'VS' 'UN' 'MAG' 'DR'
  klasius_srv vc20
  klasius_p16 vc20
  veljavnost_zac date
  veljavnost_kon date
ar_predmet
  sifra vc9
  naziv vc100
  ects num
  ure_pred num
  ure_epred num
  ure_vaj num
  ure_evaj num
  ure_labvaj num
  ind_z_prof num
  sam_delo num
  vrsta vc10 /check 'program' 'k.o.o.d.'
ar_student
  ime vc30
  priimek vc30
  vpisna num
  identiteta num
  email vc50
  sprogram num /fk ar_sprogram
  letnik vc3 /check '1' '2' '3' 'ABS' 'X'
  leto_prv_vpis date
  zac_datum date
  kon_datum date
  vrsta_vpisa vc3 /check 'red','izr','obč'
  ponavlja vc1 /check 'D','N'
ar_profesor
  ime vc30
  priimek vc30
  naziv vc35
  email vc50
  prostor_id num /fk ar_prostor
ar_namen
  opis vc30
  trajanje_minut num
ar_tip_dogodka
  opis vc25
ar_predmet_program
  letnik num
  obv_izb vc10 /check 'obvezni' 'izbirni' 
  semester vc10 /check 'zimski' 'poletni'
  predmet_id num /fk ar_predmet
  program_id num /fk ar_sprogram
ar_prof_pred
  profesor_id num /fk ar_profesor
  predmet_id num /fk ar_predmet
  zac_datum date
  kon_datum date 
ar_skupina
  naziv vc150
ar_skup_stud
  skupina_id num /fk ar_skupina
  student_id num /fk ar_student
  zac_datum date
  kon_datum date 
  vloga vc20 /check 'udeleženec' 'član' 'predsednik'
ar_gov_ure
  zac_datum date
  kon_datum date
  modif_datum date
  status_gu vc50
  url vc255
  prostor_id num /fk ar_prostor
  profesor_id num /fk ar_profesor
ar_gu_termin
  zac_datum date
  kon_datum date
  modif_datum date
  status_gu vc50
  govorilne_id num /fk ar_gov_ure
  student_id num /fk ar_student
  namen_id num /fk ar_namen
ar_urnik
  prostor_id num /fk ar_prostor
  profesor_id num /fk ar_profesor
  skupina_id num /fk ar_skupina
  predmet_id num /fk ar_predmet
  tip_dogodka_id num/fk ar_tip_dogodka
  zac_datum date
  kon_datum date
  komentar vc200
  url vc255
ar_koledar
  akad_datum date
  akad_status vc1 /check 'D' 'N'

 Non-default options:
# settings = {"apex":"Y","db":"19c"}

*/