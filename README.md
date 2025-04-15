# modif bdd
migration faisable (dire oui lors qu'on te demande de changer la date truc)
chaque modele est dans sa bonne app

pour l'app dashboard logiquement elle n'aura aucune table mais aura acces a toutes les autres, je pense que pour pouvoir y acceder il suffit de les importer dans odels et les "activer" dans admin.py de l'app.

je viens de me rendre compte que j'avais pas vérifié les models de accounts et leur admin si tu veux le faire ma n9olch lala (ma tsiyich tkassar rassek bezzaf m"ah c'est vraiiiment le dernier truc li nessah9oh)

# questions pour la suite
- est ce qu'on garde l'app evaluations ou on la fusionne avec contrats ?
- est ce que on garde blacklist dans la meme app que fournisseurs ?

# sql pour la gestion quotidienne des blacklist ( a utiliser dans toad)

ajouter les autorisations au user oracle avant.
GRANT CREATE JOB TO MON_UTILISATEUR;
GRANT MANAGE SCHEDULER TO MON_UTILISATEUR;
GRANT EXECUTE ON DBMS_SCHEDULER TO MON_UTILISATEUR;


BEGIN
  DBMS_SCHEDULER.create_job (
    job_name        => 'LEVER_LA_SANCTIONS_JOB',
    job_type        => 'PLSQL_BLOCK',
    job_action      => 'BEGIN 
                          UPDATE JURIDIQUE_FOURNISSEUR 
                          SET ETAT = ''HABILITE'',
                              DATE_EXCLUSION = NULL,
                              DUREE_EXCLUSION = NULL,
                              DATE_LEVEE_SANCTION = NULL,
                              STRUCTURE_AYANT_EXCLU = NULL
                          WHERE DATE_LEVEE_SANCTION <= SYSDATE
                          AND ETAT = ''BLACKLISTE'';
                        END;',
    start_date      => SYSTIMESTAMP,
    repeat_interval => 'FREQ=DAILY', -- Exécution quotidienne
    enabled         => TRUE,
    comments        => 'Mise à jour quotidienne des sanctions'
  );
END;
/


pour la conversion en fichier excell: 
pip install openpyxl