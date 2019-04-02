package account

import (
	"database/sql"
	"fmt"
	"time"

	"github.com/DemoHn/obsidian-panel/app/drivers/sqlite"
)

const (
	tableName     = "accounts"
	allColumns    = "id, name, credential, permission_level"
	insertColumns = "name, credential, permission_level"
)

// PermLevel - a type defines permission level constants
type PermLevel = string

const (
	// OWNER - panel owner - ownes all permissions in the panel
	// including get the details of machine, etc.
	// We will not use it currently.
	// OWNER   PermLevel = "OWNER"

	// ADMIN - administrator - ownes all permissions except those related
	// to the HOST server itself.
	ADMIN PermLevel = "ADMIN"
	// USER - normal user
	USER PermLevel = "USER"

	// VISITOR - visitor
	// VISITOR PermLevel = "VISITOR"
)

// insertAccountRecord - create Account model
func insertAccountRecord(db *sqlite.Driver, account *Account) error {
	var err error
	var stmt = fmt.Sprintf(`insert into %s (%s, created_at, updated_at) values (?, ?, ?, ?, ?)`, tableName, insertColumns)

	_, err = db.Exec(stmt,
		account.Name,
		account.Credential,
		account.PermLevel,
		time.Now(),
		time.Now(),
	)
	return err
}

// ListAccountsRecord - list account data
// notice: limit, offset can be optional
// notice2: offset only affective when limit is not null
func listAccountsRecord(db *sqlite.Driver, limit *int, offset *int) ([]Account, error) {
	var err error
	var rows *sql.Rows
	// valiation on limit
	var limitStr = ""
	var offsetStr = ""
	if limit != nil {
		if *limit < 0 {
			return nil, ValidationError("limit < 0")
		}

		limitStr = fmt.Sprintf("limit %d", *limit)
	}
	if limit != nil && offset != nil {
		if *offset < 0 {
			return nil, ValidationError("offset < 0")
		}

		offsetStr = fmt.Sprintf("offset %d", *offset)
	}

	var accounts []Account

	// query statement
	var stmt = fmt.Sprintf("select %s from %s %s %s", allColumns, tableName, limitStr, offsetStr)
	if rows, err = db.Query(stmt); err != nil {
		return nil, SQLExecutionError(err)
	}

	for rows.Next() {
		var newAccount Account
		if err = rows.Scan(&newAccount.ID, &newAccount.Name, &newAccount.Credential, &newAccount.PermLevel); err != nil {
			return nil, SQLExecutionError(err)
		}

		accounts = append(accounts, newAccount)
	}

	return accounts, nil
}

// getAccountByName - get account model by name
func getAccountByName(db *sqlite.Driver, name string) (*Account, error) {
	var err error
	var newAccount Account

	var stmt = fmt.Sprintf("select %s from %s where name = ?", allColumns, tableName)
	if err = db.QueryRow(stmt, name).Scan(
		&newAccount.ID,
		&newAccount.Name,
		&newAccount.Credential,
		&newAccount.PermLevel); err != nil {
		if err == sql.ErrNoRows {
			return nil, FindAccountError(name)
		}
		return nil, SQLExecutionError(err)
	}

	return &newAccount, nil
}