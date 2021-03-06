package providers

import (
	"github.com/DemoHn/obsidian-panel/app/drivers"
	"github.com/DemoHn/obsidian-panel/app/providers/account"
	"github.com/DemoHn/obsidian-panel/app/providers/procmanager"
	"github.com/DemoHn/obsidian-panel/app/providers/secret"
)

// Providers - define all providers
type Providers struct {
	Account        account.Provider
	ProcessManager procmanager.Provider
	Secret         secret.Provider
}

// Init - init providers
func Init(drv *drivers.Drivers) (*Providers, error) {
	sc := secret.New(drv.Sqlite)
	return &Providers{
		Account:        account.New(drv, sc),
		ProcessManager: procmanager.New(false),
		Secret:         sc,
	}, nil
}
