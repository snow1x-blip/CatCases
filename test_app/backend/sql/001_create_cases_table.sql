CREATE TABLE IF NOT EXISTS cases (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    image_path TEXT NOT NULL,
    contents JSONB NOT NULL DEFAULT '[]'::jsonb
);

INSERT INTO cases (name, image_path, contents)
SELECT
    'Starter Cat Case',
    '/images/case1.png',
    COALESCE(
        jsonb_agg(
            jsonb_build_object(
                'item_id', i.id,
                'count',
                CASE LOWER(COALESCE(i.rarity, ''))
                    WHEN 'common' THEN 50
                    WHEN 'rare' THEN 30
                    WHEN 'epic' THEN 12
                    WHEN 'legendary' THEN 5
                    ELSE 10
                END
            )
        ),
        '[]'::jsonb
    )
FROM items i
WHERE NOT EXISTS (
    SELECT 1 FROM cases c WHERE c.name = 'Starter Cat Case'
);
