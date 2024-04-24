SELECT
    [PayRollApp_employee].[id              ],
    [PayRollApp_employee].[FirstName       ],
    [PayRollApp_employee].[LastName        ],
    [PayRollApp_employee].[TitleName       ],
    [PayRollApp_employee].[HasPasport      ],
    [PayRollApp_employee].[Salary          ],
    [PayRollApp_employee].[BirthDate       ],
    [PayRollApp_employee].[HireDate        ],
    [PayRollApp_employee].[Notes           ],
    [PayRollApp_employee].[Email           ],
    [PayRollApp_employee].[PhoneNumber     ],
    [PayRollApp_employee].[EmpDepartment_id],
    [PayRollApp_employee].[EmpCountry_id   ],
    [PayRollApp_department].[id            ],
    [PayRollApp_department].[DeptName      ],
    [PayRollApp_department].[LocationName  ],
    [PayRollApp_country].[id               ],
    [PayRollApp_country].[CountryName      ]
FROM
    [PayRollApp_employee]
INNER JOIN
    [PayRollApp_department]
ON
    (
        [PayRollApp_employee].[EmpDepartment_id] = [PayRollApp_department].[id])
INNER JOIN
    [PayRollApp_country]
ON
    (
        [PayRollApp_employee].[EmpCountry_id] = [PayRollApp_country].[id])