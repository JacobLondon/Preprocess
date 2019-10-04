#define MYENTITY_DEF(name) \
    entity name is \
        Port ( \
            iClk : in std_logic; \
            o8An : out std_logic_vector (7 downto 0) \
        ); \
    end entity;
