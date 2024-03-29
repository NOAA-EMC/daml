import xarray as xr
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_squared_error
from scipy.stats import pearsonr
from matplotlib import cm
from matplotlib.gridspec import GridSpec
import cartopy.crs as ccrs
import pandas as pd

def scatterplot_ice(ax, var, varname, bounds=None, cmap='gist_ncar'):
    if (bounds is None):
        scatter = ax.scatter(lon, lat, c=var,
                             cmap=cmap, s=.5, alpha=0.8, transform=ccrs.PlateCarree())
    else:
        scatter = ax.scatter(lon, lat, c=var,
                             cmap=cmap, s=.5, alpha=0.8, transform=ccrs.PlateCarree(),
                             vmin=bounds[0], vmax=bounds[1])
    ax.coastlines()
    ax.set_title(varname)
    plt.colorbar(scatter, ax=ax, orientation='horizontal', shrink=0.5, pad=0.02)

class Ice:
    def __init__(self, filename):
        self.filename = filename
        ds = xr.open_dataset(filename)
        self.aice = ds["aice"].values
        self.aice_ffnn = ds["aice_ffnn"].values
        self.dcdt = ds["dcdt"].values
        self.dcds = ds["dcds"].values
        self.dcdsi = ds["dcdsi"].values
        self.dcdhi = ds["dcdhi"].values
        self.dcdhs = ds["dcdhs"].values
        self.dcdtair = ds["dcdtair"].values
        self.dcdtsfc = ds["dcdtsfc"].values
        self.lon = ds["lon"].values
        self.lat = ds["lat"].values

    def diff(self, other):
        self.aice -= other.aice
        self.aice_ffnn -= other.aice_ffnn

    def scatterplot_ice(self, ax, var, varname, bounds=None, cmap='viridis'):
        if (bounds is None):
            scatter = ax.scatter(self.lon, self.lat, c=var,
                                 cmap=cmap, s=.5, alpha=0.8, transform=ccrs.PlateCarree())
        else:
            scatter = ax.scatter(self.lon, self.lat, c=var,
                                 cmap=cmap, s=.5, alpha=0.8, transform=ccrs.PlateCarree(),
                                 vmin=bounds[0], vmax=bounds[1])

        ax.coastlines()
        ax.set_title(varname)
        plt.colorbar(scatter, ax=ax, orientation='horizontal', shrink=0.5, pad=0.02)

    def plotall(self):
        fig = plt.figure(figsize=(8, 8))
        gs = GridSpec(3, 3, width_ratios=[1, 1, 1], height_ratios=[1, 1, 1])

        #projection = ccrs.SouthPolarStereo()
        projection = ccrs.NorthPolarStereo()

        # Target aice
        ax1 = fig.add_subplot(gs[0, 0], projection=projection)
        #f009.scatterplot_ice(ax1, f009.aice, "$aice$", bounds=[-0.1, 0.1], cmap='RdBu_r')
        self.scatterplot_ice(ax1, self.aice, "$aice$", bounds=[0, 1])

        # Target aice
        ax2 = fig.add_subplot(gs[0, 1], projection=projection)
        #f009.scatterplot_ice(ax2, f009.aice_ffnn, "$aice_{ffnn}$", bounds=[-0.1, 0.1], cmap='RdBu_r')
        self.scatterplot_ice(ax2, self.aice_ffnn, "$aice_{ffnn}$", bounds=[0, 1])

        #plt.tight_layout()
        #plt.show()

        # Un-balanced aice
        #ax2 = fig.add_subplot(gs[0, 2], projection=projection)
        #scatterplot_ice(ax2, aice - aice_ffnn, "$aice_{u}$", bounds=[-0.1, 0.1], cmap='bwr')

        # dcdsst
        ax3 = fig.add_subplot(gs[1, 0], projection=projection)
        self.scatterplot_ice(ax3, self.dcdt, "$dc/dT_{ocean}$", cmap='PuOr', bounds=[-0.3, 0.3])

        # dcds
        ax4 = fig.add_subplot(gs[1, 1], projection=projection)
        self.scatterplot_ice(ax4, self.dcds, "$dc/dS_{ocean}$", cmap='PuOr', bounds=[-0.02, 0.02])

        # dcdsi
        ax = fig.add_subplot(gs[0, 2], projection=projection)
        self.scatterplot_ice(ax, self.dcdsi, "$dc/dS_{ice}$", cmap='PuOr', bounds=[-0.05, 0.05])

        # dcdhi
        ax5 = fig.add_subplot(gs[1, 2], projection=projection)
        self.scatterplot_ice(ax5, self.dcdhi, "$dc/dh_{ice}$", cmap='PuOr', bounds=[-3, 3])

        # dcdhs
        ax6 = fig.add_subplot(gs[2, 0], projection=projection)
        self.scatterplot_ice(ax6, self.dcdhs, "$dc/dh_{snow}$", cmap='PuOr', bounds=[-3, 3])

        # dcdtsfc
        ax = fig.add_subplot(gs[2, 1], projection=projection)
        self.scatterplot_ice(ax, self.dcdtsfc, "$dc/dT_{sfc}$", cmap='PuOr', bounds=[-0.1, 0.1])

        # dcdtair
        ax = fig.add_subplot(gs[2, 2], projection=projection)
        self.scatterplot_ice(ax, self.dcdtair, "$dc/dT_{air}$", cmap='PuOr', bounds=[-0.05, 0.05])

        plt.tight_layout()
        plt.savefig(f"{self.filename}.png")

    def densityplot(self):
        # Calculate RMSE and correlation coefficient
        rmse = np.sqrt(mean_squared_error(self.aice, self.aice_ffnn))
        corr_coef, _ = pearsonr(self.aice.flatten(), self.aice_ffnn.flatten())

        df = pd.DataFrame({"aice": self.aice, "aice_ffnn": self.aice_ffnn})

        # Create a density plot
        sns.set(style="whitegrid")
        plt.figure(figsize=(8, 8))
        resolution=15
        sns.kdeplot(data=df, x="aice", y="aice_ffnn", cmap=cm.get_cmap("jet"), fill=True,
                    common_norm=False, n_levels=resolution, common_grid=False)
        plt.xlabel("aice")
        plt.ylabel("aice_ffnn")
        plt.title(f"aice vs aice_ffnn\nRMSE: {rmse:.4f}, Correlation Coefficient: {corr_coef:.4f}")
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        plt.tight_layout()
        plt.savefig(f"{self.filename}.density.png")


# Load the NetCDF file
f009 = Ice("/home/gvernier/sandboxes/GDASApp/build/daml/gdas.t00z.icef009.ffnn.nc")
f003 = Ice("/home/gvernier/sandboxes/GDASApp/build/daml/gdas.t00z.icef003.ffnn.nc")
f003p = Ice("/home/gvernier/sandboxes/GDASApp/build/daml/gdas.t00z.20210710.icef003.ffnn.nc")
#f003 = Ice("/home/gvernier/sandboxes/GDASApp/build/daml/gdas.t00z.icef003.20210710.ffnn.nc")

#f009.diff(f003)
#f003p.densityplot()
#f003.densityplot()
#f009.densityplot()
#plt.show()

f003.plotall()
f003.densityplot()

f003p.plotall()
f003p.densityplot()

#f003.plotall()
