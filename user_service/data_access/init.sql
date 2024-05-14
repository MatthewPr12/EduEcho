DO $$
BEGIN
    -- Check if the table already exists
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_tables 
                   WHERE  schemaname = 'public' 
                   AND    tablename  = 'User') THEN
        -- Only create the table if it does not exist
        CREATE TABLE "User" (
            "UserLogin" VARCHAR(255) NOT NULL UNIQUE PRIMARY KEY,
            "UserPasswordHash" VARCHAR(255) NOT NULL,
            "UserFaculty" VARCHAR(255),
            "UserProgram" VARCHAR(255)
        );
        RAISE NOTICE 'Table created';
    ELSE
        RAISE NOTICE 'Table already exists';
    END IF;
END $$;