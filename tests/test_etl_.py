import unittest

    
class ReplaceUrlsTest(unittest.TestCase):
    def test_modify_records(self):
        source = StaticSource(
            FieldSet([
                Field( 'email', StringFieldType(), key = True ),
                Field( 'age', IntegerFieldType() )
            ],
            FieldMap({
                'email': 0,
                'age': 1
            }))
        )
        source.setResource([
            [ 'El Agent@metl-test-data.com', 12 ],
            [ 'Ochala Wild@metl-test-data.com', 14 ],
            [ 'Sina Venomous@metl-test-data.com', 17 ],
            [ 'Akassa Savage Phalloz@metl-test-data.com', 16 ],
            [ 'Sermak Bad@metl-test-data.com', 22 ],
            [ 'Olivia Deadly Dawod@metl-test-data.com', 32 ],
            [ 'PendusInhuman@metl-test-data.com', 42 ],
            [ 'Naria Cold-blodded Greste@metl-test-data.com', 22 ],
            [ 'ShardBrutal@metl-test-data.com', 54 ],
            [ 'Sina Cruel@metl-test-data.com', 56 ],
            [ 'Deadly Ohmar@metl-test-data.com', 43 ],
            [ 'Mylenedriz Cold-blodded@metl-test-data.com', 23 ],
            [ 'Calden rigid@metl-test-data.com', 35 ],
            [ 'AcidReaper@metl-test-data.com', 56 ],
            [ 'Raven Seth@metl-test-data.com', 23 ],
            [ 'RandomLeader@metl-test-data.com', 45 ],
            [ 'Pluto Brigadier@metl-test-data.com', 64 ],
            [ 'Southern Kangaroo@metl-test-data.com', 53 ],
            [ 'Serious Flea@metl-test-data.com', 62 ],
            [ 'NocturnalRaven@metl-test-data.com', 63 ],
            [ 'Risky Flea@metl-test-data.com', 21 ],
            [ 'Rivatha Todal@metl-test-data.com', 56 ],
            [ 'Panic Oliviaezit@metl-test-data.com', 25 ],
            [ 'Tomara Wild@metl-test-data.com', 46 ],
            [ 'Venessa Metalhead@metl-test-data.com', 53 ],
            [ 'Western Ogre@metl-test-data.com', 71 ],
            [ 'SergeantStrawberry@metl-test-data.com', 76 ]
        ])

        modified_record=ReplaceUrls(record)
        self.assertEqual(modified_record.getField('content'), '')
